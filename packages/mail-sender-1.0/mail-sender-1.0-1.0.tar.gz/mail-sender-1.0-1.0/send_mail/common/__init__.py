import os
from pathlib import Path
import smtplib
import re
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Callable, Literal
from ..errors import MailException, raiseMailException

class MailSender:
    '''
    Classe responsável pelo envio de e-mails
    Exemplo de utilização:

        Template foo_bar.txt:
        -------------------------------
        Olá, ${NOME_PESSOA}!

        Tudo bem!

        Tchau.
        -------------------------------
        
        class Data(MailSender):
            _HOST='0.0.0.0'
            _PORT=00
            _MAIL_USERNAME='user@teste.com.br'
            _MAIL_PASSWORD='bar'
            _FROM='rem@teste.com.br'
            _TO='dest@teste.com.br'
            _SUBJECT='Foo Bar'
            _PATH_TEMPLATE=Path('foo_bar.txt')
            _TYPE_MESSAGE = 'html'

        
        Data().send('foo')
    '''
    _HOST: Callable | str = raiseMailException('HOST não encontrado')
    _PORT: Callable | int = raiseMailException('PORT não encontrado')
    _MAIL_USERNAME: Callable | str = raiseMailException('MAIL_USERNAME não encontrado')
    _MAIL_PASSWORD: Callable | str = raiseMailException('MAIL_PASSWORD não encontrado')
    _FROM: Callable | str = raiseMailException('FROM não encontrado')
    _TO: Callable | str = raiseMailException('TO não encontrado')
    _SUBJECT: Callable | str = raiseMailException('SUBJECT não encontrado')
    _PATH_TEMPLATE: Callable | Path = raiseMailException('PATH_TEMPLATE não encontrado')
    _TYPE_MESSAGE: Literal['plain'] | Literal['html'] = 'plain'

    def __create(self, host: str, port: int, username: str, password: str):
        try:
            s = smtplib.SMTP(host, port)
            s.starttls()
            s.login(username, password)
            self.__SMTP = s
        except:
            raise MailException('Falha na conexão via SMTP')

    def send_hpupm(self, host: str, port: int, username: str, password: str, message: MIMEMultipart):
        get_headers = map(message.get ,['From', 'To', 'Subject'])
        if None in get_headers:
            raise MailException('Headers na mensagem inválidos. Necessários (From, To, Subject)')
        try:
            if not isinstance(list(message.get_payload())[0], MIMEText):
                raise MailException('Payload deve ser uma instância de email.mime.text.MIMEText')
        except IndexError:
            raise MailException('Payload vazio')
        
        if message.__dict__.get('_default_type') != 'text/plain':
            raise MailException('O type deve ser text/plain')

        self.__create(host, port, username, password)
        self.__SMTP.send_message(message)

    def send_hpom(self, host: str, port: int, message: MIMEMultipart):
        infos = [self._MAIL_USERNAME, self._MAIL_PASSWORD]
        [obj() if isinstance(obj, Callable) else None for obj in filter(lambda obj: isinstance(obj, Callable), infos)]
        self.send_hpupm(host=host, port=port, username=self._MAIL_USERNAME, password=self._MAIL_PASSWORD, message=message) # type: ignore
    
    def send_hpopp(self, host: str, port: int, path_message: Path, params: tuple[str,...]):
        if not os.path.isfile(path_message):
            raise MailException('O caminho não foi encontrado')
        with open(path_message, 'r') as file:
            message_template = file.readlines()
        get_param = lambda msg: re.search(r'\${(\w+)}', msg)
        parametros = [get_param(message) for message in message_template]
        parametros_list_str = list(map(lambda p: str(p.group(1)) ,filter(bool, parametros))) #type: ignore
        template = Template('\n'.join(message_template))
        msg = MIMEMultipart()
        message = template.substitute({param: value for param, value in zip(parametros_list_str, params)})
        infos = [self._FROM, self._TO, self._SUBJECT]
        [obj() if isinstance(obj, Callable) else None for obj in filter(lambda obj: isinstance(obj, Callable), infos)]
        msg['From'] = self._FROM
        msg['To'] = self._TO
        msg['Subject'] = self._SUBJECT
        msg.attach(MIMEText(message, self._TYPE_MESSAGE))
        self.send_hpom(host=host, port=port, message=msg)
    
    def send_hpop(self, host: str, port: int, params: tuple[str,...]):
        [obj() if isinstance(obj, Callable) else None for obj in filter(lambda obj: isinstance(obj, Callable), [self._PATH_TEMPLATE])]
        self.send_hpopp(host=host, port=port, path_message=self._PATH_TEMPLATE, params=params) # type: ignore

    def send(self, *params: str):
        infos = [self._HOST, self._PORT]
        [obj() if isinstance(obj, Callable) else None for obj in filter(lambda obj: isinstance(obj, Callable), infos)]
        self.send_hpop(host=self._HOST, port=self._PORT, params=params) # type: ignore
