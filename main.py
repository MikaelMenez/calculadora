import flet as ft
from func import *
import flet as ft
from func import *

def main(page: ft.Page):
    # Configurações da página
    page.title = "Calculadora de Equações"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "start"
    page.padding = 20
    page.theme_mode = "light"
    page.scroll = "adaptive"
    
    # Variável para controlar se é mobile
    is_mobile = ft.Ref[bool]()
    is_mobile.current = False  # Valor padrão
    
    # Componentes UI
    loading_indicator = ft.ProgressRing(width=20, height=20, stroke_width=2, visible=False)
    
    # Função para atualizar a detecção de mobile
    def update_mobile_detection():
        # Usando uma abordagem baseada no tamanho da janela
        is_mobile.current = page.width < 600 if hasattr(page, 'width') else False
        return is_mobile.current
    
    # Funções de callback
    def calcular_raizes(e):
        try:
            loading_indicator.visible = True
            btn_calcular.disabled = True
            page.update()
            
            equation = botavariavel(equacao.value)
            raizes.value = raiz(equation, 'X')
        except Exception as ex:
            raizes.value = f"Erro: {str(ex)}"
        finally:
            loading_indicator.visible = False
            btn_calcular.disabled = False
            page.update()
    
    def mostrar_explicacao(e):
        try:
            loading_indicator.visible = True
            btn_explicar.disabled = True
            page.update()
            
            explicacao_texto = explicacao(equacao.value, raizes.value)
            solucao_content.content = ft.Text(
                value=explicacao_texto,
                size=16,
                selectable=True,
            )
            grafico.src = ""
            grafico.visible = False
            solucao_header.value = "Explicação Detalhada:"
        except Exception as ex:
            solucao_content.content = ft.Text(
                value=f"Erro ao gerar explicação: {str(ex)}",
                size=16,
            )
        finally:
            loading_indicator.visible = False
            btn_explicar.disabled = False
            page.update()
    
    def mostrar_grafico(e):
     try:
        loading_indicator.visible = True
        btn_grafico.disabled = True
        page.update()
        
        # Gera e exibe o gráfico
        grafico.src_base64 = cria_grafico(equacao.value)
        grafico.visible = True
        solucao_header.value = f"Gráfico de {equacao.value}"
        solucao_content.visible = False
        
     except Exception as ex:
        solucao_header.value = f"Erro ao gerar gráfico: {str(ex)}"
        grafico.visible = False
     finally:
        loading_indicator.visible = False
        btn_grafico.disabled = False
        page.update()
    # Atualiza o layout quando a página é carregada ou redimensionada
    def on_page_resize(e):
        update_mobile_detection()
        btn_grafico.visible = not is_mobile.current
        page.update()
    
    page.on_resize = on_page_resize
    
    # Componentes da UI
    titulo = ft.Text(
        "Calculadora de Equações",
        size=28,
        weight="bold",
        text_align="center"
    )
    
    subtitulo = ft.Text(
        "Insira uma equação e clique nos botões para calcular raízes ou explicação",
        size=14,
        text_align="center"
    )
    
    equacao = ft.TextField(
        label="Digite sua equação (ex: x^2 - 4)",
        width=400,
        text_size=16,
        content_padding=10,
    )
    
    raizes = ft.Text(
        value="",
        size=18,
        selectable=True,
        text_align="center"
    )
    
    solucao_header = ft.Text(
        value="",
        size=18,
        weight="bold",
        text_align="center"
    )
    
    solucao_content = ft.Container(
        content=ft.Text(""),
        padding=15,
        border_radius=10,
        width=600,
        height=300,

    )
    
    grafico = ft.Image(
        src_base64="",  # Alterado de src para src_base64
        width=400,
        height=300,
        fit=ft.ImageFit.CONTAIN,
        visible=False,
        border_radius=10,
    )    
    # Botões
    btn_calcular = ft.ElevatedButton(
        "Calcular Raízes",
        on_click=calcular_raizes,
        icon=ft.Icons.CALCULATE,
        style=ft.ButtonStyle(
            padding=20,
        )
    )
    
    btn_explicar = ft.ElevatedButton(
        "Explicação",
        on_click=mostrar_explicacao,
        icon=ft.Icons.HELP_OUTLINE,
        style=ft.ButtonStyle(
            padding=20,)
    )
    
    btn_grafico = ft.ElevatedButton(
        "Mostrar Gráfico",
        on_click=mostrar_grafico,
        icon=ft.Icons.INSERT_CHART,
        style=ft.ButtonStyle(
            padding=20,
        )
    )
    
    botoes = ft.Row(
        [btn_calcular, btn_explicar],
        alignment="center",
        spacing=10,
        wrap=True
    )
    
    # Layout principal
    page.add(
        ft.Column(
            [
                titulo,
                subtitulo,
                ft.Divider(height=20),
                equacao,
                ft.Divider(height=10),
                ft.Row([botoes,ft.Divider(height=20)], alignment="center"),
                ft.Divider(height=10),
                btn_grafico,
                loading_indicator,
                ft.Divider(height=20),
                ft.Container(
                    content=raizes,
                    padding=10,
                    border_radius=10,
                    width=400
                ),
                ft.Divider(height=20),
                solucao_header,
                solucao_content,
                ft.Divider(height=20),
                grafico
            ],
            spacing=0,
            horizontal_alignment="center",
        )
    )
    
    # Atualização inicial
    def on_page_load(e):
        update_mobile_detection()
        btn_grafico.visible = not is_mobile.current
        page.update()
    
    page.on_load = on_page_load

if __name__ == "__main__":
    ft.app(target=main)
