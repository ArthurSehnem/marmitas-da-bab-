import streamlit as st
import urllib.parse
from typing import Dict, List
from dataclasses import dataclass

# =========================
# MODELOS DE DADOS
# =========================
@dataclass
class Produto:
    """Modelo para representar um produto"""
    nome: str
    descricao: str
    peso: str
    preco: float
    imagem: str = None
    categoria: str = "dia_a_dia"

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="Marmitas da Babá",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# ESTADO GLOBAL
# =========================
def init_session_state():
    """Inicializa o estado da sessão"""
    if "carrinho" not in st.session_state:
        st.session_state.carrinho = {}
    
    if "show_toast" not in st.session_state:
        st.session_state.show_toast = False
    
    if "toast_message" not in st.session_state:
        st.session_state.toast_message = ""

init_session_state()

# =========================
# DADOS DOS PRODUTOS
# =========================
PRODUTOS_DIA_A_DIA = [
    Produto(
        nome="Frango grelhado com arroz, feijão e legumes",
        descricao="Arroz branco (100g), feijão (100g), filé de frango grelhado (130g) e mix de legumes (100g).",
        peso="430g",
        preco=22.00,
        imagem="images/frango.jpg"
    ),
    Produto(
        nome="Carne moída com arroz, feijão e moranga",
        descricao="Arroz branco (100g), feijão (100g), carne moída (130g) e purê de moranga cabotiá (100g).",
        peso="430g",
        preco=22.00,
        imagem="images/carne_moida.png"
    ),
    Produto(
        nome="Penne com iscas de alcatra e legumes",
        descricao="Massa penne (100g), iscas de alcatra (130g) e mix de legumes (120g).",
        peso="350g",
        preco=20.00,
        imagem="images/penne_alcatra.jpg"
    ),
    Produto(
        nome="Penne com carne moída e legumes",
        descricao="Massa penne (100g), carne moída (130g) e mix de legumes (120g).",
        peso="350g",
        preco=20.00,
        imagem="images/penne_carne.jpg"
    ),
    Produto(
        nome="Alcatra com arroz e purê de moranga",
        descricao="Arroz branco (100g), iscas de alcatra (130g) e purê de moranga cabotiá (120g).",
        peso="350g",
        preco=20.00,
        imagem="images/alcatra_moranga.png"
    ),
    Produto(
        nome="Frango cremoso com arroz e legumes",
        descricao="Arroz branco (100g), iscas de frango cremoso (130g) e mix de legumes (120g).",
        peso="350g",
        preco=20.00,
        imagem="images/frango_cremoso.jpg"
    )
]

PRODUTOS_ESCONDIDINHOS = [
    Produto(
        nome="Escondidinho de carne de panela com aipim",
        descricao="Carne de panela desfiada (150g) com aipim cremoso (200g).",
        peso="350g",
        preco=23.00,
        categoria="escondidinhos",
        imagem = "images/escondidinho-carne-panela.png"
    ),
    Produto(
        nome="Escondidinho de frango desfiado com aipim",
        descricao="Frango desfiado temperado (150g) com aipim cremoso (200g).",
        peso="350g",
        preco=23.00,
        categoria="escondidinhos",
        imagem = "images/escondidinho-carne-panela.png"

    ),
    Produto(
        nome="Escondidinho de carne de panela com moranga",
        descricao="Carne de panela desfiada (150g) com purê de moranga cabotiá (200g).",
        peso="350g",
        preco=23.00,
        categoria="escondidinhos",
        imagem = "images/escondidinho-carne-panela.png"

    ),
    Produto(
        nome="Escondidinho de carne moída com moranga",
        descricao="Carne moída bem temperada (150g) com purê de moranga cabotiá (200g).",
        peso="350g",
        preco=23.00,
        categoria="escondidinhos",
        imagem = "images/escondidinho-carne-panela.png"

    ),
    Produto(
        nome="Escondidinho de carne de panela com batata inglesa",
        descricao="Carne de panela desfiada (150g) com purê de batata inglesa (200g).",
        peso="350g",
        preco=23.00,
        categoria="escondidinhos",
        imagem = "images/escondidinho-carne-panela.png"

    ),
    Produto(
        nome="Escondidinho de frango desfiado com batata inglesa",
        descricao="Frango desfiado temperado (150g) com purê de batata inglesa (200g).",
        peso="350g",
        preco=23.00,
        categoria="escondidinhos",
        imagem = "images/escondidinho-carne-panela.png"

    ),
    Produto(
        nome="Escondidinho de carne moída com batata inglesa",
        descricao="Carne moída refogada (150g) com purê de batata inglesa (200g).",
        peso="350g",
        preco=23.00,
        categoria="escondidinhos",
        imagem = "images/escondidinho-carne-panela.png"


    )
]

# =========================
# FUNÇÕES DO CARRINHO
# =========================
def adicionar_ao_carrinho(produto: Produto) -> None:
    """Adiciona um produto ao carrinho"""
    nome = produto.nome
    
    if nome in st.session_state.carrinho:
        st.session_state.carrinho[nome]["quantidade"] += 1
    else:
        st.session_state.carrinho[nome] = {
            "preco": produto.preco,
            "quantidade": 1
        }
    
    st.session_state.toast_message = f"✓ {nome} adicionado!"
    st.session_state.show_toast = True


def alterar_quantidade(nome: str, delta: int) -> None:
    """Altera a quantidade de um item no carrinho"""
    if nome in st.session_state.carrinho:
        st.session_state.carrinho[nome]["quantidade"] += delta
        
        if st.session_state.carrinho[nome]["quantidade"] <= 0:
            del st.session_state.carrinho[nome]


def limpar_carrinho() -> None:
    """Limpa todos os itens do carrinho"""
    st.session_state.carrinho = {}
    st.session_state.toast_message = "🗑️ Carrinho limpo!"
    st.session_state.show_toast = True


def calcular_total() -> float:
    """Calcula o total do carrinho"""
    return sum(
        item["preco"] * item["quantidade"]
        for item in st.session_state.carrinho.values()
    )


def contar_itens() -> int:
    """Conta o número total de itens no carrinho"""
    return sum(
        item["quantidade"]
        for item in st.session_state.carrinho.values()
    )

# =========================
# ESTILOS CSS
# =========================
def aplicar_estilos():
    """Aplica os estilos CSS customizados"""
    st.markdown("""
    <style>
    /* Remove underline e highlight das tabs */
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-bottom: none !important;
    }

    .stTabs [data-baseweb="tab"] > div {
        border-bottom: none !important;
    }

    /* Container das tabs */
    div[data-baseweb="tab-list"] {
        display: flex;
    }

    /* Força o container das tabs a ocupar 100% */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        width: 100%;
    }

    /* Cada tab ocupa o mesmo espaço */
    .stTabs [data-baseweb="tab"] {
        flex: 1 !important;
        text-align: center;
        justify-content: center;
        background: white;
        color: #3d2817;
        border-radius: 10px;
        font-weight: 600;
        border: 1px solid rgba(212,165,116,0.4);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg,#d4a574,#c29560);
        color: white;
    }

    /* Fundo */
    body {
        background-color: #faf8f5;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #FBF5F2;
    }

    section[data-testid="stSidebar"] * {
        color: #362A22 !important;
    }

    /* Produtos */
    .product-row {
        padding-top: 16px !important;
        padding-bottom: 16px;
        border-bottom: 1px solid rgba(212,165,116,0.2);
    }

    /* Força as colunas do Streamlit a ficarem centralizadas verticalmente */
    .product-row > div[data-testid="column"] {
        display: flex !important;
        align-items: center !important;
    }

    /* Remove espaçamento superior da imagem */
    .product-row img {
        display: block;
        border-radius: 14px;
        width: 100%;
        height: auto;
        object-fit: cover;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Container da imagem */
    .product-row [data-testid="column"]:first-child > div {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

    /* Botões dos produtos */
    .stButton > button {
        background-color: white;
        color: #362A22;
        border: 2px solid #E5D8CC;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: white !important;
        color: #362A22 !important;
        border-color: #C29560 !important;
    }

    .stButton > button:active,
    .stButton > button:focus,
    .stButton > button:focus-visible {
        background-color: white !important;
        color: #362A22 !important;
        border-color: #B8894E !important;
        box-shadow: none !important;
    }

    .product-name {
        font-weight: 600;
        color: #3d2817;
        margin-bottom: 8px;
    }

    .product-description {
        font-size: 0.8rem;
        color: #6b5744;
        line-height: 1.4;
    }

    .product-weight {
        font-size: 0.75rem;
        font-style: italic;
        color: #8b7355;
        margin-top: 4px;
    }

    .product-price {
        font-size: 1.1rem;
        font-weight: 700;
        color: #d4a574;
        margin: 8px 0;
    }

    /* Toast */
    .toast {
        position: fixed;
        top: 80px;
        right: 20px;
        background: #d4a574;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        z-index: 9999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease;
    }

    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    /* Carrinho */
    .cart-qty {
        font-size: 1.1rem;
        font-weight: 700;
        color: #3d2817;
        text-align: center;
    }

    .cart-total {
        font-size: 1.6rem;
        font-weight: 700;
        color: #d4a574;
        text-align: right;
        margin: 20px 0;
    }

    .cart-badge {
        background: #d4a574;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 8px;
    }

    /* WhatsApp */
    .whatsapp-button {
        background: linear-gradient(135deg,#d4a574,#c29560);
        color: white !important;
        padding: 1rem;
        border-radius: 14px;
        font-weight: 600;
        text-align: center;
        display: block;
        margin-top: 1rem;
        text-decoration: none;
        transition: all 0.3s ease;
    }

    .whatsapp-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212,165,116,0.4);
    }

    /* Botão limpar carrinho */
    .clear-cart-button {
        background: transparent;
        color: #d4a574;
        border: 1px solid #d4a574;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .clear-cart-button:hover {
        background: #fef8f3;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================
# COMPONENTES UI
# =========================
def mostrar_toast():
    """Exibe notificação toast"""
    if st.session_state.show_toast:
        st.markdown(f"""
        <div class="toast">{st.session_state.toast_message}</div>
        <script>
            setTimeout(() => {{
                const t = document.querySelector('.toast');
                if (t) t.remove();
            }}, 2000);
        </script>
        """, unsafe_allow_html=True)
        st.session_state.show_toast = False


def renderizar_produto(produto: Produto):
    """Renderiza um card de produto"""
    st.markdown("<div class='product-row'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 3.5])
    
    with col1:
        if produto.imagem:
            try:
                st.image(produto.imagem, width=160)
            except Exception:
                st.markdown("🍱", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div class='product-name'>{produto.nome}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='product-description'>{produto.descricao}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='product-weight'>Peso: {produto.peso}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='product-price'>R$ {produto.preco:.2f}</div>", unsafe_allow_html=True)
        
        st.button(
            "＋ Adicionar",
            key=f"add_{produto.nome}",
            on_click=adicionar_ao_carrinho,
            args=(produto,),
            use_container_width=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)


def renderizar_sidebar():
    """Renderiza a sidebar com informações"""
    with st.sidebar:
        try:
            st.image("images/logo.png", use_container_width=True)
        except Exception:
            st.markdown("# 🍱 Marmitas da Babá")
        
        st.markdown("""
        ### 📋 Como funciona
        1️⃣ Escolha as marmitas  
        2️⃣ Adicione ao carrinho  
        3️⃣ Finalize no WhatsApp  
        
        📸 @marmitasdababa  
        📞 (51) 99887-0311
        """)
        
        # Badge do carrinho na sidebar
        num_itens = contar_itens()
        if num_itens > 0:
            st.markdown(f"""
            ---
            ### 🛒 Carrinho
            **{num_itens}** {'item' if num_itens == 1 else 'itens'}  
            **R$ {calcular_total():.2f}**
            """)


def renderizar_carrinho():
    """Renderiza o carrinho de compras"""
    if not st.session_state.carrinho:
        return
    
    st.markdown("## 🛒 Seu Pedido")
    
    for nome, item in list(st.session_state.carrinho.items()):
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        
        with col1:
            subtotal = item['preco'] * item['quantidade']
            st.markdown(f"**{nome}**  \n{item['quantidade']}x • R$ {item['preco']:.2f}")
        
        with col2:
            st.button("➖", key=f"menos_{nome}", on_click=alterar_quantidade, args=(nome, -1))
        
        with col3:
            st.markdown(f"<div class='cart-qty'>{item['quantidade']}</div>", unsafe_allow_html=True)
        
        with col4:
            st.button("➕", key=f"mais_{nome}", on_click=alterar_quantidade, args=(nome, 1))
    
    # Total e botões
    col1, col2 = st.columns([3, 1])
    
    with col1:
        total = calcular_total()
        st.markdown(f"<div class='cart-total'>Total: R$ {total:.2f}</div>", unsafe_allow_html=True)
    
    with col2:
        st.button("🗑️ Limpar", on_click=limpar_carrinho, use_container_width=True)
    
    # Botão WhatsApp
    gerar_botao_whatsapp()


def gerar_botao_whatsapp():
    """Gera o botão de finalização via WhatsApp"""
    mensagem = "Olá! Gostaria de fazer o pedido:\n\n"
    
    for nome, item in st.session_state.carrinho.items():
        mensagem += f"• {item['quantidade']}x {nome} - R$ {item['preco'] * item['quantidade']:.2f}\n"
    
    total = calcular_total()
    mensagem += f"\n*Total: R$ {total:.2f}*"
    
    link = "https://wa.me/5551998870311?text=" + urllib.parse.quote(mensagem)
    
    st.markdown(
        f"<a href='{link}' target='_blank' class='whatsapp-button'>📲 Finalizar no WhatsApp</a>", 
        unsafe_allow_html=True
    )

# =========================
# APLICAÇÃO PRINCIPAL
# =========================
def main():
    """Função principal da aplicação"""
    # Aplicar estilos
    aplicar_estilos()
    
    # Mostrar toast se necessário
    mostrar_toast()
    
    # Renderizar sidebar
    renderizar_sidebar()
    
    # Cabeçalho
    st.title("🍱 Marmitas Personalizadas!")

    st.markdown("""
*Envie sua dieta ou plano alimentar, e suas marmitas serão preparadas exatamente conforme suas orientações, respeitando quantidades, ingredientes e restrições.* *Não tem dieta pronta? Sem problema! Disponibilizo opções de refeições que podem ser escolhidas e adaptadas ao seu gosto e objetivo.*
""")

    st.markdown("""
*Observação: Quantidades e ingredientes podem ser ajustados conforme sua preferência, podendo haver pequeno ajuste no valor da marmita. Tudo é combinado com carinho e transparência.*
""")

    st.markdown("---")
    
    # Tabs de produtos
    tab1, tab2 = st.tabs(["🍽️ Dia a Dia", "🥘 Escondidinhos"])
    
    with tab1:
        for produto in PRODUTOS_DIA_A_DIA:
            renderizar_produto(produto)
    
    with tab2:
        for produto in PRODUTOS_ESCONDIDINHOS:
            renderizar_produto(produto)
    
    # Carrinho
    st.markdown("---")
    renderizar_carrinho()
    
    # Rodapé
    st.markdown("---")
    st.caption("💻 Feito com carinho por Arthur Sehnem")


if __name__ == "__main__":
    main()