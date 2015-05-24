#!/usr/bin/python

import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.logger import Logger


class PopupOperacaoWidget(Popup):

    valor_deposito = 0.0

    def __init__(self, **kwargs):
        self.title = "Operacao: " + str(kwargs['title_operacao'])
        self.text_button_efetuar_operacao = str(kwargs['text_button_operacao'])
        self.callback = kwargs['callback']
        super(PopupOperacaoWidget, self).__init__(**kwargs)

    def on_press_efetuar_operacao(self):
        self.callback(self.valor_deposito)
        self.dismiss()

    def on_text_update_valor(self, valor):
        self.valor_deposito = valor


class PopupAlertaWidget(Popup):

    def __init__(self, **kwargs):
        self.title = kwargs['text_title_alerta']
        self.text_label_alerta = kwargs['text_label_alerta']
        self.text_button_retorno = kwargs['text_button_retorno']
        super(PopupAlertaWidget, self).__init__(**kwargs)


class BancoNacionalWidget(BoxLayout):

    valor_saldo_disponivel = NumericProperty(0.0)
    text_display_saldo = StringProperty("")

    def __init__(self, **kwargs):
        super(BancoNacionalWidget, self).__init__(**kwargs)
        self.update_text_display_saldo()

    def update_text_display_saldo(self):
        self.text_display_saldo = "Saldo disponivel: R$ " + str(self.valor_saldo_disponivel)

    def increment_saldo_disponivel(self, valor):
        __validated_value = self.validate_valor_passado(valor)
        if __validated_value:
            self.valor_saldo_disponivel += __validated_value
            self.update_text_display_saldo()

    def decrement_saldo_disponivel(self, valor):
        __validated_value = self.validate_valor_passado(valor)
        if __validated_value:
            self.valor_saldo_disponivel -= __validated_value
            self.update_text_display_saldo()

    def on_press_operacao_depositar(self, *args):
        popup_depositar = PopupOperacaoWidget(
            title_operacao="Depositar",
            text_button_operacao="Efetuar Deposito!",
            callback=self.increment_saldo_disponivel).open()

    def on_press_operacao_sacar(self, *args):
        popup_sacar = PopupOperacaoWidget(
            title_operacao="Sacar",
            text_button_operacao="Efetuar Saque!",
            callback=self.validate_saldo_disponivel).open()


    def validate_saldo_disponivel(self, valor_saque):
        __validated_value = self.validate_valor_passado(valor_saque)
        if __validated_value:
            if self.valor_saldo_disponivel - __validated_value < 0:
                popup_valor_indisponivel = PopupAlertaWidget(
                    text_title_alerta = "Operacao invalida:",
                    text_label_alerta = "Saldo indisponivel para saque!",
                    text_button_retorno = "Voltar ao menu principal").open()
            else:
                self.decrement_saldo_disponivel(__validated_value)


    def validate_valor_passado(self, valor):
        try:
            return float(valor)
        except:
            popup_valor_invalido = PopupAlertaWidget(
                text_title_alerta = "Operacao invalida:",
                text_label_alerta = "O valor passado invalido!",
                text_button_retorno = "Voltar ao menu principal").open()
            return None

    def on_press_operacao_cancelar(self, *args):
        sys.exit(1)


class BancoNacionalApp(App):

    def build(self):
        return BancoNacionalWidget()

if __name__ == "__main__":
    __version__ = "0.1.0"
    BancoNacionalApp().run()
