import asyncio
from collections.abc import Callable
import re
import fnmatch
from pathlib import Path, PurePath
import imaplib
import aiofiles
from flowtask.conf import IMAP_RETRY_SELECT
from flowtask.utils.mail import MailMessage
from flowtask.exceptions import ComponentError, FileNotFound
from .DownloadFrom import DownloadFromBase
from settings.settings import FILES_PATH
from .IMAPClient import IMAPClient


class DownloadFromIMAP(IMAPClient, DownloadFromBase):

    """
    DownloadFromIMAP.

    Overview

            Download emails from an IMAP mailbox

    .. table:: Properties
       :widths: auto


    +-------------------+----------+-----------+---------------------------------------+
    | Name              | Required | Summary                                           |
    +-------------------+----------+-----------+---------------------------------------+
    | credentials       |   Yes    | Credentials from IMAP mailbox                     |
    +-------------------+----------+-----------+---------------------------------------+
    | mailbox           |   Yes    | The buzón IMAP , by default INBOX                 |
    +-------------------+----------+-----------+---------------------------------------+
    | search terms      |   Yes    | Searches in IMAP format                           |
    +-------------------+----------+-----------+---------------------------------------+
    | attachments       |   Yes    | Directory to download the files                   |
    +-------------------+----------+-----------+---------------------------------------+
    | download_existing |   Yes    | If true, file that already detect is downloaded is|
    |                   |          | downloaded again                                  |
    +-------------------+----------+-----------+---------------------------------------+
    | results           |   Yes    | attachments: list of attached files               |
    |                   |          | messages: body content de MailMessages            |
    +-------------------+----------+-----------+---------------------------------------+

    Return the list of arbitrary days

    """
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ) -> None:
        self.attachments = {
            "directory": None
        }
        self.search_terms = None
        DownloadFromBase.__init__(
            self,
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        params = self._params.copy()
        IMAPClient.__init__(
            self,
            **params
        )
        self.create_destination: bool = True  # by default

    def start(self, **kwargs):  # pylint: disable=W0613
        if hasattr(self, 'attachments'):
            # attachment directory
            if 'directory' not in self.attachments:
                self.attachments['directory'] = FILES_PATH.joinpath(
                    self._program, 'files', 'download'
                )
            else:
                self.attachments['directory'] = Path(
                    self.attachments['directory']
                ).resolve()
            try:
                directory = self.attachments['directory']
                if not directory.exists():
                    if self.create_destination is True:
                        directory.mkdir(parents=True, exist_ok=True)
                    else:
                        raise ComponentError(
                            f'DownloadFromIMAP: Error creating directory: {directory}'
                        )
            except Exception as err:
                self._logger.error(
                    f'IMAP: Error creating directory: {err}'
                )
                raise ComponentError(
                    f'IMAP: Error creating directory: {err}'
                ) from err
            # masking elements:
            if hasattr(self, 'masks'):
                for mask, replace in self._mask.items():
                    for key, val in self.attachments.items():
                        value = str(val).replace(mask, str(replace))
                        if isinstance(val, PurePath):
                            self.attachments[key] = Path(value)
                        else:
                            self.attachments[key] = value
        return super(DownloadFromIMAP, self).start()

    async def run(self):
        self._result = None
        filter_criteria = []
        msgs = ['']
        messages = []
        files: list = []
        try:
            await self.open(
                self.host, self.port, self.credentials
            )
            if not self._client:
                raise ComponentError(
                    "IMAP Connection not Opened, exiting."
                )
        except Exception as err:
            self._logger.exception(err, stack_info=True)
            raise
        # getting search Terms
        self.search_terms = self.process_mask('search_terms')
        for term, value in self.search_terms.items():
            try:
                value = self.mask_replacement(value)
                filter_criteria.append(f'({term} "{value}")')
            except (ValueError, KeyError):
                pass
        self._logger.debug(f'FILTER CRITERIA: {filter_criteria}')
        self.add_metric("SEARCH", filter_criteria)
        try:
            # getting the Mailbox
            self._client.select(self.mailbox)
        except Exception as err:
            if 'User is authenticated but not connected.' in str(err):
                tries = 0
                while tries < IMAP_RETRY_SELECT:
                    self._client.logout()
                    await asyncio.sleep(10)
                    try:
                        await self.open(self.host, self.port, self.credentials)
                        if not self._client:
                            raise ComponentError(
                                "IMAP Connection not Opened, exiting."
                            ) from err
                        self._client.select(self.mailbox)
                        break
                    except Exception as exc:
                        self._logger.exception(exc, stack_info=True)
                        if tries < (IMAP_RETRY_SELECT - 1):
                            tries += 1
                            continue
                        else:
                            raise RuntimeError(
                                f'IMAP: Error opening Mailbox {self.mailbox}: {exc}'
                            ) from exc
        try:
            print('FILTER ', filter_criteria)
            result, msgs = self._client.search(None, *filter_criteria)
            if result == 'NO' or result == 'BAD':
                self._logger.error(msgs[0])
                raise ComponentError(
                    message=f'Error on Search: {msgs[0]}',
                    code=500
                )
        except imaplib.IMAP4.abort as err:
            raise ComponentError(
                f'IMAP Illegal Search: {err}'
            ) from err
        except Exception as err:
            self._logger.exception(err, stack_info=True)
            raise ComponentError(
                f'IMAP Error: {err}'
            ) from err
        msgs = msgs[0].split()
        i = 0
        if not msgs:
            raise FileNotFound(
                "DownloadFromIMAP: File(s) doesn't exists"
            )
        if not isinstance(msgs, list):
            raise ComponentError(
                f"DownloadFromIMAP: Invalid Email Response: {msgs}"
            )
        if 'expected_mime' in self.attachments:
            expected_mime = self.attachments['expected_mime']
            if expected_mime:
                validate_mime = True
            else:
                validate_mime = False
        else:
            expected_mime = None
            validate_mime = False
        for emailid in msgs:
            i += 1
            resp, data = self._client.fetch(emailid.decode("utf-8"), "(RFC822)")
            if resp == 'OK':  # mail was retrieved
                msg = MailMessage(
                    self.attachments['directory'],
                    data[0][1].decode('utf-8'),
                    data[1],
                    validate_mime=validate_mime
                )
                messages.append(msg)
                for attachment in msg.attachments:
                    if expected_mime is not None:
                        # checking only for valid MIME types:
                        if expected_mime != attachment['content_type']:
                            continue
                    if 'filename' in self.attachments:
                        fname = self.attachments['filename']  # we only need to save selected files
                        if not fnmatch.fnmatch(attachment['filename'], fname):
                            continue
                        else:
                            if 'rename' in self.attachments:
                                filename = self.attachments['rename']
                                filename = filename.replace(
                                    '{filename}', Path(attachment['filename']).stem
                                )
                                self._logger.debug(f'NEW FILENAME IS {filename}')
                                file_path = self.attachments['directory'].joinpath(filename)
                            else:
                                file_path = self.attachments['directory'].joinpath(attachment['filename'])
                    elif 'pattern' in self.attachments:  # only save files that match the pattern
                        fpattern = self.attachments['pattern']
                        if bool(re.match(fpattern, attachment['filename'])):
                            file_path = self.attachments['directory'].joinpath(attachment['filename'])
                        else:
                            continue
                    else:
                        # I need to save everything
                        if 'rename' in self.attachments:
                            filename = self.attachments['rename']
                            if hasattr(self, 'masks'):
                                for mask, replace in self._mask.items():
                                    filename = filename.replace(mask, replace)
                            filename = filename.replace('{filename}', Path(attachment['filename']).stem)
                            file_path = self.attachments['directory'].joinpath(filename)
                        else:
                            file_path = self.attachments['directory'].joinpath(attachment['filename'])
                    # saving the filename in the attachment
                    attachment['filename'] = file_path
                    if 'download_existing' in self.attachments:
                        if file_path.exists() and self.attachments['download_existing'] is False:
                            # we don't need to download again
                            self._logger.info(f'File Exists {file_path!s}, skipping')
                            continue
                    if file_path.exists() and self.overwrite is False:
                        # TODO: before to save a new renamed file,
                        #  we need to check if we have it (checksum)
                        file_name = file_path.name
                        # dir_name = file_path.absolute()
                        ext = file_path.suffix
                        # calculated new filepath
                        file_path = self.attachments['directory'].joinpath(f'{file_name}_{i}{ext}')
                        if file_path.exists():
                            # TODO: more efficient way (while) to check if file exists
                            files.append(file_path)
                            continue
                    await self.save_attachment(file_path, attachment['attachment'])
                    # saving this file in the list of files:
                    files.append(file_path)
            else:
                raise ComponentError(
                    f'File was not fetch: {resp}'
                )
        # saving the result:
        self.add_metric("ATTACHMENTS", files)
        # self.add_metric("Messages", messages)
        self._result = {
            "messages": messages,
            "files": files
        }
        return self._result

    async def save_attachment(self, file_path, content):
        try:
            self._logger.info(
                f'IMAP: Saving attachment file: {file_path}'
            )
            async with aiofiles.open(file_path, mode='wb') as fp:
                await fp.write(content)
        except Exception as err:
            raise ComponentError(
                f'File {file_path} was not saved: {err}'
            ) from err
