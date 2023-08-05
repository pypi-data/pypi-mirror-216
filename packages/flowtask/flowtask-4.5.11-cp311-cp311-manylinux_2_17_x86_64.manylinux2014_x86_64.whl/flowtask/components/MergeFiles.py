import os
import logging
import asyncio
from collections.abc import Callable
import types
import pandas as pd
import numpy as np
import cchardet as chardet
# from flowtask.utils import *
from flowtask.exceptions import ComponentError
from flowtask.parsers.maps import open_model
from .abstract import DtComponent

excel_based = (
    "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
    "application/vnd.ms-excel.sheet.macroEnabled.12",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
    "text/xml"
)

class MergeFiles(DtComponent):
    """
    MergeFiles

    Overview

           Merges one or more files into a single file optionally this merge can be
           returned as a dataframe

    .. table:: Properties
       :widths: auto


    +---------------+----------+-----------+-------------------------------------------+
    | Name          | Required | Summary                                               |
    +---------------+----------+-----------+-------------------------------------------+
    | as_dataframe  |   Yes    | Is True a Pandas Dataframe is returned, otherwise a   |
    |               |          | file is returned                                      |
    +---------------+----------+-----------+-------------------------------------------+
    | ContentType   |   Yes    | MIME file type, if you want to save a file to         |
    |               |          | disk text/csv - application/vd-ms-excel               |
    +---------------+----------+-----------+-------------------------------------------+
    | destination   |   Yes    | Directory and file name                               |
    +---------------+----------+-----------+-------------------------------------------+


    Return the list of arbitrary days
    """
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ) -> None:
        """Init Method."""
        self.filename = ''
        self.file = None
        self.filepath = ''
        self.ContentType: str = "text/csv"
        self.as_dataframe: bool = False
        super(MergeFiles, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs):
        """
        start.
            Start connection.
        """
        if self.previous:
            try:
                if isinstance(self.input, list):
                    # is a list of files
                    self.data = self.input
                elif isinstance(self.input, dict):
                    if 'files' in self.input:
                        self.data = self.input['files']
                    else:
                        self.data = {k: v for k, v in self.input.items()}
                elif isinstance(self.input, types.GeneratorType):
                    # is a generator:
                    self.data = list(self.input)
                else:
                    raise ComponentError(
                        "MergeFiles Error: incompatible kind of previous Object."
                    )
            except Exception as err:
                raise ComponentError(
                    f"Error Filtering Data {err}"
                ) from err
        self._logger.debug(
            f'List of Files: {self.data!r}'
        )
        if hasattr(self, 'destination'):
            # we need to calculated the result filename of this component
            filename = self.destination['filename']
            self.filepath = self.destination['directory']
            if hasattr(self, 'masks'):
                for mask, replace in self._mask.items():
                    filename = str(filename).replace(mask, replace)
            if self._variables:
                filename = filename.format(**self._variables)
            self.filename = os.path.join(self.filepath, filename)
            self.add_metric('MERGED_FILENAME', self.filename)
        return True

    async def close(self):
        """
        close.

            close method
        """

    async def run(self):
        """
        run.

            Run the connection and merge all the files
        """
        np_array_list = []
        df = None
        np_array_list = []
        if isinstance(self.data, list):
            # is a list of files
            if self.ContentType in excel_based:
                args = {}
                if hasattr(self, 'pd_args'):
                    args = self.pd_args
                if self.ContentType == "application/vnd.ms-excel":
                    file_engine = 'xlrd'
                elif self.ContentType == 'application/vnd.ms-excel.sheet.binary.macroEnabled.12':
                    file_engine = 'pyxlsb'
                else:
                    file_engine = 'openpyxl'
                # get the Model (if any):
                if hasattr(self, 'model'):
                    columns = await open_model(self.model, self._program)
                    fields = []
                    dates = []
                    for field, dtype in columns['fields'].items():
                        fields.append(field)
                        try:
                            t = dtype['data_type']
                        except KeyError:
                            t = 'str'
                        if t in ('date', 'datetime', 'time'):
                            dates.append(field)
                    args['names'] = fields
                    if dates:
                        args['parse_dates'] = dates
                files = []
                for file in self.data:
                    if not file:
                        continue
                    try:
                        df = pd.read_excel(
                            file,
                            na_values=['TBD', 'NULL', 'null', '', '#NA'],
                            engine=file_engine,
                            keep_default_na=True,
                            **args
                        )
                    except TypeError as ex:
                        self._logger.error(
                            f"Merge Excel Error: {ex}"
                        )
                    files.append(df)
                try:
                    self._result = pd.concat(
                        files
                    )
                    if self._debug is True:
                        print('::: Combined File ::: ')
                        print(self._result)
                    if self.as_dataframe is True:
                        numrows = len(self._result)
                        self.add_metric('NUMROWS', numrows)
                        self.add_metric('COLUMNS', self._result.shape[1])
                        return self._result
                    else:
                        # saved as CSV.
                        self._result.to_csv(
                            self.filename,
                            index=False,
                            encoding='utf-8-sig'
                        )
                        self._result = self.filename
                        self.add_metric('MERGED_FILE', self.filename)
                    return self._result
                except Exception as err:
                    logging.exception(
                        f'Error Merging Excel Files: {err}',
                        stack_info=True
                    )
                    self._result = None
                    return False
            elif self.ContentType == "text/html":
                encoding = "utf-8"
                try:
                    if len(self.data) == 1:
                        # there is no other files to merge:
                        combined_csv = pd.read_html(self.data[0], encoding=encoding)
                    else:
                        dfs = []
                        for f in self.data:
                            try:
                                dt = pd.read_html(f, encoding=encoding)
                                dfs.append(dt[0])
                            except (TypeError, ValueError):
                                continue
                        # combine all files in the list
                        combined_csv = pd.concat(
                            dfs, sort=False, axis=0, ignore_index=True
                        ).reindex(dfs[0].index)
                except UnicodeDecodeError:
                    combined_csv = pd.concat(
                        [pd.read_html(f, encoding='windows-1252') for f in self.data]
                    )
                except Exception as err:
                    raise ComponentError(f"{err!s}") from err
                try:
                    if self.as_dataframe is True:
                        self._result = combined_csv
                        self.add_metric('MERGED_DF', self._result.columns)
                    else:
                        # export to csv
                        combined_csv.to_csv(
                            self.filename,
                            index=False,
                            encoding='utf-8-sig'
                        )
                        self._result = self.filename
                        self.add_metric('MERGED_FILE', self.filename)
                    return self._result
                except Exception as err:
                    logging.error(err)
                    self._result = None
                    return False
            elif self.ContentType == "text/csv":
                try:
                    encoding = None
                    for file in self.data:
                        buffer = None
                        with open(file, 'rb') as f:
                            buffer = f.read(10000)
                        result_charset = chardet.detect(buffer)
                        enc = result_charset['encoding']
                        if encoding is not None and enc != encoding:
                            logging.warning(
                                'MergeFiles: files has different encoding'
                            )
                        encoding = enc
                    if encoding == 'ASCII':
                        encoding = "utf-8-sig"
                except Exception as err:
                    logging.warning(
                        f'MergeFiles: DECODING ERROR {err}'
                    )
                    encoding = "utf-8-sig"
                try:
                    if len(self.data) == 1:
                        # there is no other files to merge:
                        combined_csv = pd.read_csv(self.data[0], encoding=encoding)
                    else:
                        # combine all files in the list
                        combined_csv = pd.concat(
                            [pd.read_csv(f, encoding=encoding) for f in self.data]
                        )
                    print(f'COMBINED CSV: {combined_csv}')
                except UnicodeDecodeError:
                    combined_csv = pd.concat(
                        [pd.read_csv(f, encoding='windows-1252') for f in self.data]
                    )
                except Exception as err:
                    raise ComponentError(f"{err!s}") from err
                try:
                    if self.as_dataframe is True:
                        self._result = combined_csv
                        self.add_metric('MERGED_DF', self._result.columns)
                    else:
                        # export to csv
                        combined_csv.to_csv(
                            self.filename,
                            index=False,
                            encoding='utf-8-sig'
                        )
                        self._result = self.filename
                        self.add_metric('MERGED_FILE', self.filename)
                    return self._result
                except Exception as err:
                    self._logger.error(err)
                    self._result = None
                    return False
        elif isinstance(self.data, dict):
            for f in self.data:
                ip = self.data[f]['data']
                if self.ContentType == "application/json":
                    if self.data[f]['type'] == 'binary/octet-stream':
                        # wrapper = io.TextIOWrapper(input, encoding='utf-8')
                        content = ip.getvalue()
                    else:
                        # convert to string:
                        # wrapper = io.TextIOWrapper(input, encoding='utf-8')
                        content = ip
                    # content = wrapper.read()
                    df = pd.read_json(content, orient='records')
                    columns = list(df.columns)
                    np_array_list.append(df.values)
                comb_np_array = np.vstack(np_array_list)
                df = pd.DataFrame(comb_np_array)
                df.columns = columns
            self._result = df
            return True
        else:
            self._result = None
            return False
