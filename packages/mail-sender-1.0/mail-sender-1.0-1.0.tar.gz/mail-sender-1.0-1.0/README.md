# Mail Sender

> Classe responsável pelo envio de e-mails

**Crie um template**
Template foo_bar.txt:
-------------------------------
Olá, ${NOME_PESSOA}!

Tudo bem!

Tchau.
-------------------------------

**Crie uma classe para definir os atributos principais**    
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

**Chame o método _send()_ para enviar**
Exemplo de utilização:
    Data().send('foo')