import streamlit as st
import json
import base64
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="택배 분쟁 전문 도우미",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern premium glassmorphism and gradient styles
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    /* Main container and font */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Noto Sans KR', 'Outfit', sans-serif;
        background: radial-gradient(circle at 10% 20%, rgba(90, 92, 234, 0.08) 0%, rgba(255, 255, 255, 0) 100%), 
                    radial-gradient(circle at 90% 80%, rgba(252, 176, 69, 0.05) 0%, rgba(255, 255, 255, 0) 100%),
                    #0f172a;
        color: #f8fafc;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Headers styling */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .main-title {
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #fb7185 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Glassmorphism Card Wrapper */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.15);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    /* Form inputs and buttons styling */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.6);
        transform: scale(1.02);
    }
    
    /* Claim copy block styling */
    .claim-box {
        background-color: #0b0f19;
        border-left: 4px solid #6366f1;
        border-radius: 4px 8px 8px 4px;
        padding: 20px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 0.95rem;
        line-height: 1.6;
        color: #e2e8f0;
        margin: 15px 0;
        white-space: pre-wrap;
    }
    
    /* Responsibility meter styling */
    .responsibility-bar-container {
        width: 100%;
        background-color: #334155;
        border-radius: 10px;
        height: 20px;
        display: flex;
        overflow: hidden;
        margin: 15px 0;
    }
    
    .res-courier {
        background-color: #6366f1;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.75rem;
        font-weight: bold;
    }
    
    .res-seller {
        background-color: #10b981;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.75rem;
        font-weight: bold;
    }
    
    .res-buyer {
        background-color: #f59e0b;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.75rem;
        font-weight: bold;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 5px;
    }
    .badge-courier { background-color: rgba(99, 102, 241, 0.2); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.4); }
    .badge-seller { background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
    .badge-buyer { background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Main Banner / Header
st.markdown('<div class="main-title">📦 택배 분쟁 해결 전문 도우미</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">소비자의 권익을 대변하여 상황을 철저히 분석하고, 즉시 사용할 수 있는 클레임 서신과 대응 전략을 드립니다.</div>', unsafe_allow_html=True)

# Helper function to generate PDF download (Text based layout)
def get_txt_download_link(filename, text, link_text):
    b64 = base64.b64encode(text.encode('utf-8')).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}" style="color: #818cf8; text-decoration: underline; font-weight: 600;">{link_text}</a>'

# Initialize session states
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = {}

# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🛠️ 분석 설정")
    ai_mode = st.checkbox("AI 심층 분석 모드 활성화", value=False, help="Gemini API를 사용하여 입력한 서술에 대해 더 세밀하고 개인화된 법적 조언과 클레임을 작성합니다.")
    
    gemini_key = ""
    if ai_mode:
        gemini_key = st.text_input("Gemini API Key", type="password", help="Gemini API 키를 입력해주세요. 입력된 키는 로컬 세션에서만 안전하게 사용됩니다.")
        st.markdown("[API 키 발급받기](https://aistudio.google.com/)")
    
    st.markdown("---")
    st.markdown("### 💡 주요 법률 정보")
    with st.expander("상법 제135조 (손해배상책임)"):
        st.caption("운송인은 자기 또는 운송주선인이나 사용인, 그 밖에 운송을 위하여 사용한 자가 운송물의 수령, 인도, 보관 및 운송에 관하여 주의를 게을리하지 아니하였음을 증명하지 아니하면 운송물의 멸실, 훼손 또는 연착으로 인한 손해를 배상할 책임을 면하지 못합니다.")
    with st.expander("공정위 택배표준약관 제20조"):
        st.caption("택배사는 운송물의 분실, 파손 또는 배송 지연에 대해 물품 가액 및 배송비를 기준으로 산정된 손해배상 책임을 집니다.")
    with st.expander("전자상거래법 제13조 (배송책임)"):
        st.caption("통신판매업자(인터넷 쇼핑몰)는 소비자에게 상품을 인도하기 전까지 발생한 상품의 분실, 파손에 대한 책임을 부담합니다. 따라서 소비자는 쇼핑몰을 상대로 직접 환불이나 재발송을 청구할 권리가 있습니다.")

# Main input forms
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📝 피해 상황 정보 입력")
    
    # Common input fields
    purchase_type = st.radio(
        "🛒 상품 구매처 구분",
        options=["인터넷 쇼핑몰 (쿠팡, 네이버쇼핑 등)", "개인 간 거래 (당근마켓, 중고나라 등)", "개인 발송 물품 (선물, 이사짐 등)"],
        index=0
    )
    
    dispute_type = st.selectbox(
        "🔍 분쟁 피해 유형 선택",
        options=["택배 분실 (배송 완료되었으나 받지 못함)", "택배 파손 (파손/침수/오염 등)", "배송 지연 (약정일 초과, 신선식품 변질 등)", "오배송 (타 주소지 배송, 수령인 오류 등)"]
    )
    
    # Dynamic Questionnaire based on selected dispute type
    st.markdown("---")
    st.markdown("#### ⚙️ 세부 조건 선택")
    
    details = {}
    
    if "분실" in dispute_type:
        details['confirm_message'] = st.radio(
            "1. 배송 완료 안내(문자, 알림톡 등)를 받으셨나요?",
            options=["예 (사진 또는 문자가 왔음)", "아니오 (무단 완료 처리 또는 알림이 없었음)"]
        )
        details['consent'] = st.radio(
            "2. 문 앞 등 특정 장소 방치에 사전에 동의(요청)하셨나요?",
            options=["아니오 (동의한 적 없거나 대면 수령을 원했음, 혹은 연락 없이 방치됨)", "예 (배송 요청사항에 '문 앞' 등을 선택함)"]
        )
        details['check_places'] = st.checkbox("경비실, 택배 보관함, 옆집 등을 확인해 보셨습니까?")
        
    elif "파손" in dispute_type:
        details['external_damage'] = st.radio(
            "1. 외부 택배 박스 자체에 손상이 보이나요?",
            options=["예 (상자가 찢어짐, 젖음, 찌그러짐 등 흔적이 있음)", "아니오 (상자는 멀쩡하나 내부 알맹이만 파손됨)"]
        )
        details['cushioning'] = st.radio(
            "2. 판매자의 내부 포장 상태가 적절했나요?",
            options=["예 (완충재나 뽁뽁이가 잘 싸여 있었음)", "아니오 (완충재가 없거나 매우 부족했음)"]
        )
        details['photos_kept'] = st.checkbox("외부 상자, 내부 포장재, 파손된 제품 사진을 모두 촬영해 두셨습니까?")
        
    elif "지연" in dispute_type:
        details['item_nature'] = st.radio(
            "1. 배송 물품의 성격이 무엇인가요?",
            options=["신선식품 / 부패성 제품 (고기, 생선, 농산물 등)", "일반 공산품 (의류, 가전 등)", "중요 서류 또는 특정 일시가 지나면 쓸모없는 물품"]
        )
        details['delay_days'] = st.number_input("2. 예정 배송일로부터 며칠이 지났습니까?", min_value=1, max_value=30, value=3)
        details['damaged_by_delay'] = st.radio(
            "3. 지연으로 인해 가치가 훼손되었습니까?",
            options=["예 (식품이 부패함, 행사 일정이 지남 등)", "아니오 (도착이 늦어 기분이 상했으나 상품은 멀쩡함)"]
        )
        
    elif "오배송" in dispute_type:
        details['address_check'] = st.radio(
            "1. 운송장(또는 주문내역)에 기재된 주소가 내 주소와 일치하나요?",
            options=["예 (내 주소가 올바르게 적혀 있음 -> 택배사의 오배송)", "아니오 (주문 시 내 주소를 잘못 기재함 -> 구매자 과실)"]
        )
        details['misdelivered_photo'] = st.radio(
            "2. 택배사가 오배송 증빙(엉뚱한 집 앞 배송 사진 등)을 남겼습니까?",
            options=["예 (사진이 있음/확인됨)", "아니오 (배송 완료 상태이나 증거가 없음)"]
        )
    
    st.markdown("---")
    st.markdown("#### 💰 금액 및 기본 정보")
    item_name = st.text_input("📦 물품명", placeholder="예: 아이폰 15 Pro, 한우 선물세트 등")
    item_price = st.number_input("💰 물품 금액 (원)", min_value=0, step=1000, value=50000, help="보상액 산정의 기준이 되므로 실제 영수증/구매가액을 입력해주세요.")
    courier_company = st.selectbox("🚚 담당 택배사", options=["CJ대한통운", "우체국택배", "한진택배", "롯데택배", "로젠택배", "기타 / 모름"])
    tracking_number = st.text_input("📋 운송장 번호 (선택)", placeholder="예: 123456789012")
    
    st.markdown("#### 📝 구체적인 피해 상황 서술")
    user_story = st.text_area(
        "상황을 자세히 적어주시면 더 적합한 문구를 생성하는 데 도움이 됩니다.",
        placeholder="예: 어제 퇴근 후 문 앞을 확인했는데 택배가 와있지 않았습니다. 운송장번호 조회 시 배송 완료로 되어있고 완료 시간은 오후 2시입니다. 배송 기사님께 연락을 드렸으나 확인 후 연락 주겠다는 말만 하고 하루째 무시하고 있습니다. 쇼핑몰에서 구매한 새 신발입니다.",
        height=150
    )
    
    analyze_btn = st.button("⚖️ 분쟁 상황 분석 및 솔루션 생성")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- Core Analysis & Engine -----------------
def analyze_dispute_locally(purchase_type, dispute_type, details, item_name, item_price, courier_company, tracking_number, user_story):
    res_courier, res_seller, res_buyer = 0, 0, 0
    analysis_text = ""
    regulations = []
    claim_template = ""
    strategies = []
    
    item_name_formatted = item_name if item_name else "해당 물품"
    tracking_str = f" (운송장 번호: {tracking_number})" if tracking_number else ""
    price_formatted = f"{item_price:,}원"
    
    # 1. LOST CASE
    if "분실" in dispute_type:
        confirm_msg = details.get('confirm_message', '')
        consent = details.get('consent', '')
        
        # Determine fault
        if "인터넷 쇼핑몰" in purchase_type:
            # Under Electronic Commerce Act, seller has liability until delivery is completed to consumer.
            # But we must analyze the relation.
            if "아니오" in consent: # No consent to leave at door
                res_courier = 80
                res_seller = 20  # Seller is responsible to consumer first, then subrogates claim to courier
                res_buyer = 0
                analysis_text = f"**[분석 결과: 택배사 및 판매자 책임 극대화]**<br>" \
                                f"소비자가 문 앞 방치 등에 동의하지 않았음에도 택배기사가 임의로 물건을 두고 가 분실이 발생했습니다.<br>" \
                                f"1. **전자상거래법 제13조 제2항**: 인터넷 쇼핑몰(판매자)은 물품이 소비자에게 최종 인도될 때까지의 배송 위험을 집니다. 따라서 구매자는 택배사가 아닌 '쇼핑몰'에 직접 환불이나 재발송을 청구해야 합니다.<br>" \
                                f"2. **상법 제135조 및 택배표준약관 제20조**: 택배사는 수령인에게 물품을 대면 인도하거나 합의된 장소에 보관하지 않은 임의 방치 과실이 명백하여, 쇼핑몰에 물품 배상 책임이 있습니다."
                regulations = [
                    "전자상거래 등에서의 소비자보호에 관한 법률 제13조 (배송 책임)",
                    "공정거래위원회 택배표준약관 제20조 (수탁물 인도 의무 및 배상)",
                    "상법 제135조 (운송인의 손해배상책임)"
                ]
            else: # Buyer consented to leave at door
                res_courier = 10
                res_seller = 10
                res_buyer = 80
                analysis_text = f"**[분석 결과: 구매자 과실 일부 인정]**<br>" \
                                f"구매자가 배송 메시지나 요청사항을 통해 '문 앞' 배송에 사전 동의한 상황에서 분실된 경우, 원칙적으로 인도 의무가 완수된 것으로 보아 구매자가 피해를 떠안을 가능성이 높습니다.<br>" \
                                f"다만, 택배기사가 배송 완료 사실을 소비자에게 알리지 않았거나 오배송했을 가능성이 있다면 택배사의 불완전 이행 책임을 물을 여지가 일부 존재합니다."
                regulations = [
                    "공정거래위원회 택배표준약관 제20조",
                    "민법 제390조 (채무불이행과 손해배상)"
                ]
        else: # Used item or Individual to Individual
            if "아니오" in consent:
                res_courier = 100
                res_seller = 0
                res_buyer = 0
                analysis_text = f"**[분석 결과: 택배사 책임 100%]**<br>" \
                                f"개인 간 배송의 경우, 판매자가 발송을 완료한 후에는 배송의 책임이 전적으로 택배사로 이전됩니다.<br>" \
                                f"구매자가 문 앞 배송에 사전 동의한 사실이 없음에도 무단 방치하여 분실되었으므로, **상법 제135조**에 의거해 운송인(택배사)이 100% 손해를 배상해야 합니다."
                regulations = [
                    "상법 제135조 (운송인의 손해배상책임)",
                    "택배표준약관 제20조 (운송물의 분실에 따른 배상)"
                ]
            else:
                res_courier = 20
                res_seller = 0
                res_buyer = 80
                analysis_text = f"**[분석 결과: 구매자 과실 다분]**<br>" \
                                f"소비자가 직접 '문 앞 방치'를 수락하였기 때문에 배송 완료 시점 이후의 분실 건은 구매자의 위험 부담 영역입니다.<br>" \
                                f"하지만 배송 시 배송기사가 완료 사진이나 연락을 전혀 하지 않은 채 장시간 방치되었다면 택배사에 도의적/일부 불성실 이행 책임(약 10~20%)을 물어 합의를 유도해볼 수 있습니다."
                regulations = [
                    "민법 상의 위험부담 원칙"
                ]

        # Generate claim text
        if "인터넷 쇼핑몰" in purchase_type:
            claim_template = f"제목: [주문번호 관련] 배송 완료 미수령 및 분실에 따른 환불(재발송) 요청\n\n" \
                             f"안녕하세요. {purchase_type.split(' ')[0]} 쇼핑몰 고객님.\n" \
                             f"구매한 물품 '{item_name_formatted}'의 배송 상태가 완료로 표시되나, 실제 물품을 수령하지 못해 연락 드립니다.\n\n" \
                             f"1. 주문정보\n" \
                             f" - 상품명: {item_name_formatted}\n" \
                             f" - 구매금액: {price_formatted}\n" \
                             f" - 배송정보: {courier_company}{tracking_str}\n\n" \
                             f"2. 현황 분석 및 법적 책임 소재\n" \
                             f" - 본인은 문 앞 배송 등 무단 방치에 사전에 동의한 사실이 없으며, 상품을 수령하지 못하였습니다.\n" \
                             f" - 전자상거래법 제13조 제2항에 의거, 통신판매업자는 상품이 소비자에게 도달하기 전까지 멸실·훼손 책임이 있습니다.\n" \
                             f" - 이에 따라 귀사(판매처)에 정중히 조사와 함께 주문 금액 {price_formatted} 전액에 대한 환불 또는 신속한 재발송 처리를 요구합니다.\n\n" \
                             f"3. 향후 조치\n" \
                             f" - 원만한 해결이 어려울 경우, 전자상거래법 위반으로 한국소비자원 피해 구제 신청 및 국민신문고를 통해 공정거래위원회 제보 조치를 진행할 예정입니다.\n\n" \
                             f"고객의 과실이 전혀 없는 미수령 건이므로 신속하고 합리적인 처리를 부탁드립니다.\n\n" \
                             f"작성자: 구매자 배상"
        else:
            claim_template = f"제목: {courier_company} 배송 무단방치 분실에 대한 사고 접수 및 배상 청구\n\n" \
                             f"귀사의 무궁한 발전을 기원합니다.\n" \
                             f"본인은 보내는 분이 발송한 운송장번호 {tracking_number if tracking_number else '[운송장번호 기재]'} 물품의 수령인입니다.\n\n" \
                             f"1. 피해 현황\n" \
                             f" - 물품명: {item_name_formatted}\n" \
                             f" - 물품 가액: {price_formatted}\n" \
                             f" - 배송 현황: {courier_company}에 의해 배송완료 처리되었으나 미수령 상태\n\n" \
                             f"2. 청구 사유 및 근거 법령\n" \
                             f" - 수령인은 해당 물품을 '문 앞 방치'하도록 동의하거나 요청한 적이 없습니다.\n" \
                             f" - 그럼에도 담당 배송기사는 대면 인도하지 않고 무단으로 문 앞에 두고 감으로써 물품 분실을 야기하였습니다.\n" \
                             f" - 이는 상법 제135조(운송인의 주의의무) 및 택배표준약관 제20조에 위배되는 배송 과실입니다. 운송인은 운송물 수령·보관·인도 시 주의를 게을리하지 않았음을 입증하지 못하면 책임을 면할 수 없습니다.\n" \
                             f" - 따라서 물품 가액 {price_formatted}과 배송비 전액에 대해 100% 손해 배상을 정식으로 청구합니다.\n\n" \
                             f"3. 요청 사항\n" \
                             f" - 신속하게 운송물 사고 접수를 진행해주시고 담당 배송기사와의 확인을 거쳐 배상 절차(사고 승인)를 안내해 주시기 바랍니다.\n" \
                             f" - 본 건이 원만히 처리되지 않을 시, 국토교통부 및 한국소비자원에 민원을 정식 제기하여 과실 책임을 끝까지 물을 것임을 밝힙니다.\n\n" \
                             f"수령인: [성함 입력]"

        strategies = [
            "**1단계 (고객센터 정식 접수)**: 쇼핑몰(인터넷 쇼핑몰인 경우) 또는 택배사 고객센터에 '사고 처리 정식 접수'를 진행하세요. 구두 통화뿐만 아니라 1:1 상담 게시판 등 기록이 남는 서면 접수를 병행해야 배송사고 사실(14일 이내 의사표시) 입증이 유리합니다.",
            "**2단계 (증빙 확보 및 입증 책임)**: 아파트 복도 CCTV, 공동현관 출입 기록 등을 확인하여 택배 기사가 방문한 내역이나 실제 두고 간 사실이 있는지 증빙을 요청해 두세요. 만약 택배 기사가 배송 완료 장소의 사진을 남기지 않았다면 택배사에 배송 의무 완료 미입증 책임을 적극적으로 밀어붙여야 합니다.",
            "**3단계 (소비자원 구제 및 국토부 민원)**: 합의 거부 시, 소비자 보호 규정(물품가액 전액 배상)을 근거로 **한국소비자원(국번없이 1372)**에 피해구제를 신청하십시오. 택배사가 고의로 회피할 경우, **국민신문고**를 통해 국토교통부에 불친절 및 택배 표준약관 위반 민원을 제기하는 것이 실질적 압박이 됩니다."
        ]

    # 2. DAMAGED CASE
    elif "파손" in dispute_type:
        ext_damage = details.get('external_damage', '')
        cushioning = details.get('cushioning', '')
        
        if "예" in ext_damage: # External box damaged
            res_courier = 90
            res_seller = 10
            res_buyer = 0
            analysis_text = f"**[분석 결과: 택배사 과실 지배적]**<br>" \
                            f"박스가 찌그러지거나 찢어지는 등 외부 충격 흔적이 뚜렷합니다. 이는 운송 과정 중 취급 부주의(던짐, 적재 불량)로 인한 파손으로 분류됩니다.<br>" \
                            f"**상법 제135조**에 따라 택배사는 불가항력적인 사고였음을 직접 증명하지 못하는 한 수탁물 파손 책임을 면하기 어렵습니다."
            regulations = [
                "상법 제135조 (운송인의 책임)",
                "택배표준약관 제20조 (파손 배상 기준)"
            ]
        else: # Box clean, internal damaged
            if "아니오" in cushioning: # Poor packaging
                res_courier = 20
                res_seller = 80
                res_buyer = 0
                analysis_text = f"**[분석 결과: 판매자 포장 부실 책임]**<br>" \
                                f"택배 외관 박스는 멀쩡한데 내용물만 파손되었고, 판매자가 완충재를 제대로 넣지 않은 경우입니다.<br>" \
                                f"택배 약관상 포장 부실은 택배사의 면책 사유에 해당할 수 있어, 실질적으로 포장 불량에 책임이 있는 '판매자'를 대상으로 손해배상(교환/환불)을 청구해야 합니다."
                regulations = [
                    "민법 제390조 (채무불이행에 따른 판매자 책임)",
                    "전자상거래법 제13조 제2항"
                ]
            else:
                res_courier = 50
                res_seller = 50
                res_buyer = 0
                analysis_text = f"**[분석 결과: 책임 경합 필요]**<br>" \
                                f"외관은 정상이지만 내부 완충포장도 적절했음에도 불구하고 물품이 깨진 상황입니다. 운송 시의 미세한 고주파 진동이나 낙하 등의 문제일 수 있습니다.<br>" \
                                f"소비자가 쇼핑몰에서 산 제품이라면 전자상거래법 배송책임에 따라 쇼핑몰이 1차 책임을 지고 우선 처리(환불/교환)해야 합니다."
                regulations = [
                    "전자상거래법 제13조",
                    "소비자분쟁해결기준"
                ]

        # Generate claim text
        if "인터넷 쇼핑몰" in purchase_type:
            claim_template = f"제목: [주문번호 관련] 배송 상품 파손에 따른 교환 및 환불 신청\n\n" \
                             f"안녕하세요. {purchase_type.split(' ')[0]} 고객센터 담당자님.\n" \
                             f"주문한 상품이 파손된 상태로 도착하여 정식으로 교환/환불을 요청합니다.\n\n" \
                             f"1. 주문정보\n" \
                             f" - 상품명: {item_name_formatted}\n" \
                             f" - 금액: {price_formatted}\n" \
                             f" - 배송번호: {courier_company}{tracking_str}\n\n" \
                             f"2. 파손 상태\n" \
                             f" - [상황 기술: 예) 박스 외부가 훼손되어 있었고 내용물인 그릇이 산산조각 나 있었습니다. 관련 사진 첨부합니다.]\n\n" \
                             f"3. 청구 근거\n" \
                             f" - 전자상거래법 제13조 제2항에 따라, 소비자가 상품을 실질적으로 온전하게 인도받기 전까지의 위험 책임은 통신판매업자에게 있습니다.\n" \
                             f" - 설령 택배사의 배송 중 부주의나 포장 유통상의 원인이라 할지라도, 쇼핑몰이 소비자에게 우선적으로 조치를 취한 뒤 택배사에 구상권을 청구하는 것이 타당합니다.\n" \
                             f" - 이에 파손된 상품의 수거 및 신속한 [새 제품 교환 또는 결제 취소]를 요구합니다.\n\n" \
                             f"사진 첨부와 함께 요청드리오니, 조속히 회신 바랍니다.\n\n" \
                             f"구매자: [성함]"
        else:
            claim_template = f"제목: {courier_company} 운송물 파손 사고 접수 및 배상 청구서\n\n" \
                             f"수탁자(택배사) 귀중.\n" \
                             f"본인은 귀사가 배송한 운송장번호 {tracking_number if tracking_number else '[운송장 번호]'} 물품의 파손 피해를 입어 손해배상을 청구합니다.\n\n" \
                             f"1. 사고 개요\n" \
                             f" - 물품명: {item_name_formatted}\n" \
                             f" - 물품 가액: {price_formatted}\n" \
                             f" - 파손 상태: [예) 상자가 강하게 눌린 흔적이 있으며, 내부 액정 유리가 파손됨]\n\n" \
                             f"2. 배상 책임의 근거\n" \
                             f" - 상법 제135조에 따라 운송인은 운송물 보관 및 운송 과정에서 주의를 다했음을 입증하지 못하면 멸실·훼손의 책임을 집니다.\n" \
                             f" - 물품 상자의 파손 및 내부 가치 상실이 명확히 확인되므로, 택배표준약관 제20조에 의거하여 물품 가액 {price_formatted} 전액 배상을 요구합니다.\n\n" \
                             f"3. 증빙 자료\n" \
                             f" - 파손 박스 외관 사진 및 파손된 제품 사진 확보 중\n" \
                             f" - 구매 증빙 영수증(가액 증빙)\n\n" \
                             f"지체 없이 사고 심사를 진행하시어 본 보상건을 승인해 주시기 바랍니다.\n\n" \
                             f"청구인: [성함]"

        strategies = [
            "**1단계 (현 상태 그대로 보존 및 촬영)**: 제품 파손을 확인하는 즉시 절대 포장재나 박스를 버리지 마십시오. 송장이 붙어 있는 상자 전체 샷, 내부 포장 상태, 제품 파손 부위 상세 사진을 다각도로 촬영해야 합니다. 박스를 버리면 택배사에서 보상을 전면 거부할 수 있습니다.",
            "**2단계 (이의제기 기한 엄수)**: **택배표준약관 제22조**에 따라 파손 사실을 발송물 인도일로부터 **14일 이내**에 택배사에 서면/전화 통지해야 손해배상청구권이 유지됩니다. 기한이 지나면 택배사 면책 조항이 발동됩니다.",
            "**3단계 (구상권 청구 종용)**: 쇼핑몰 구매 건의 경우 쇼핑몰이 '택배사 책임'이라며 떠넘기더라도 단호하게 거부하십시오. 소비자 분쟁 해결 원칙상 인터넷 쇼핑몰이 소비자에게 선배상 및 환불을 해준 후, 쇼핑몰이 택배사로 구상권을 청구하는 것이 원칙입니다. 쇼핑몰 고객센터장급으로 이관을 요청하여 선환불을 받아내세요."
        ]

    # 3. DELAY CASE
    elif "지연" in dispute_type:
        nature = details.get('item_nature', '')
        delay_days = details.get('delay_days', 1)
        damaged = details.get('damaged_by_delay', '')
        
        if "신선식품" in nature and "예" in damaged:
            res_courier = 100
            res_seller = 0
            res_buyer = 0
            analysis_text = f"**[분석 결과: 신선식품 부패로 인한 택배사 100% 과실 책임]**<br>" \
                            f"냉장/냉동 배송이 요구되는 신선식품이 택배 지연으로 부패한 경우, 상품 가치를 상실했으므로 배송 지연에 귀책이 있는 택배사가 100% 손해를 배상해야 합니다.<br>" \
                            f"택배 표준 약관에 근거해 물품가액 및 운송장 비용 전액 청구가 가능합니다."
            regulations = [
                "공정위 택배표준약관 제20조 제2항 (인도 예정일 초과)",
                "소비자분쟁해결기준 (품목별 배상 기준)"
            ]
        else:
            res_courier = 80
            res_seller = 0
            res_buyer = 20
            analysis_text = f"**[분석 결과: 배송 지연 배상금 청구 가능]**<br>" \
                            f"일반 물품의 경우, 지연으로 인해 상품 자체가 망가지지 않았다면 정신적 피해보상은 법적으로 매우 어렵습니다.<br>" \
                            f"하지만 **택배 표준약관 제20조 2항**에 따라 일반 배송 지연에 대해서도 배송 지연일수에 따라 운송장 수수료(운임)의 배상금 청구가 가능합니다.<br>" \
                            f"*(배상액 계산 공식: 초과일수 × 택배비의 50%. 최대 운임의 200% 한도)*"
            regulations = [
                "택배표준약관 제20조 제2항 (배송지연 배상률 규정)"
            ]

        # Generate claim text
        claim_template = f"제목: {courier_company} 배송지연에 따른 수탁물 피해 손해배상 청구\n\n" \
                         f"담당자 귀하.\n" \
                         f"귀사를 통해 운송 중인 물품(운송장번호: {tracking_number if tracking_number else '[번호]'})의 배송 지연으로 심각한 피해가 발생하여 손해배상을 청구합니다.\n\n" \
                         f"1. 상품 및 배송 사실\n" \
                         f" - 물품명: {item_name_formatted} (가액: {price_formatted})\n" \
                         f" - 접수일자: [접수일 기재]\n" \
                         f" - 배송 예정일: [예정일 기재] (실제 완료일: {delay_days}일 지연)\n\n" \
                         f"2. 피해 상황 및 법적 근거\n" \
                         f" - 본 제품은 [선택 상황 기술: 예) 신선도가 필수적인 식품으로 배송지연기간 중 완전히 부패·변질되어 폐기해야 하는 상태입니다.]\n" \
                         f" - 택배표준약관 제20조 제2항에 따라 운송물이 인도예정일을 초과하여 연착된 경우, 수탁자는 인도 지연으로 발생한 소비자의 손해를 배상해야 합니다.\n" \
                         f" - 따라서 물품 가액 {price_formatted} 및 배송비 전액을 즉시 변제해 주실 것을 청구합니다.\n\n" \
                         f"3. 회신 요구\n" \
                         f" - 신속한 배상 의사결정을 요청드리며, 합리적인 수준의 전액 배상이 지체될 시 소비자원 피해구제 및 정부 부처 신문고 민원을 제기하겠습니다.\n\n" \
                         f"청구인: [성함]"

        strategies = [
            "**1단계 (지연 및 훼손 물품 보존)**: 신선식품인 경우, 배송된 즉시 상했음을 보여주는 사진(변색, 곰팡이, 물 생김, 온도가 다 녹은 아이스팩 등)을 찍어두고 제품은 당분간 버리지 말고 밀봉하여 냉동 보관해두십시오. 택배사 실사 시 증거물이 필요할 수 있습니다.",
            "**2단계 (지연 지체 일수 계산 및 영수증 증빙)**: 일반물품 배송지연의 경우, 택배 지연 지체료(배송비의 최대 2배)를 받기 위해 송장접수일과 수령일을 기재한 캡처본을 제출하여 청구하십시오.",
            "**3단계 (신고 접수)**: 배송 지연으로 상한 음식물의 보상을 미루거나 배송 기사의 무책임한 답변이 이어질 경우, 한국소비자원에 즉시 피해 구제를 제기하며 지연 일수 증빙 캡처 화면과 상품 실물 사진을 증거 자료로 첨부하세요."
        ]

    # 4. MISDELIVERY CASE
    else:
        addr_check = details.get('address_check', '')
        
        if "예" in addr_check:
            res_courier = 100
            res_seller = 0
            res_buyer = 0
            analysis_text = f"**[분석 결과: 택배사 오배송 100% 과실 책임]**<br>" \
                            f"구매자는 정상 주소를 입력하였으나 택배사가 엉뚱한 주소지에 물품을 배송 완료하여 분실된 상태입니다.<br>" \
                            f"택배사가 지정된 수령 장소로의 완벽한 인도 의무를 해태한 것(상법 제135조 위반)이므로, 전적으로 택배사의 과실에 따른 배상 의무가 있습니다."
            regulations = [
                "상법 제135조 (운송인의 책임)",
                "택배표준약관 제20조"
            ]
        else:
            res_courier = 0
            res_seller = 0
            res_buyer = 100
            analysis_text = f"**[분석 결과: 구매자 주소 오입력 과실 100%]**<br>" \
                            f"소비자가 배송 정보를 오입력하여 다른 주소지로 배송이 완료된 경우입니다.<br>" \
                            f"이 경우 택배사와 판매자는 면책되며, 구매자는 오배송된 주소의 거주자에게 연락하여 돌려받아야 합니다.<br>" \
                            f"만약 오배송지 거주자가 물품 반환을 거부하거나 무단 취득했을 경우 형법상 점유이탈물횡령죄가 성립될 수 있으므로 사법적 조치를 고려해야 합니다."
            regulations = [
                "형법 제360조 (점유이탈물횡령죄)"
            ]

        # Generate claim text
        if "예" in addr_check:
            claim_template = f"제목: {courier_company} 오배송 건에 대한 즉각적 수거 또는 물품 배상 요구\n\n" \
                             f"운송인(택배사) 담당자님.\n" \
                             f"본인은 귀사에서 배송 완료 처리한 운송장 {tracking_number if tracking_number else '[번호]'} 물품의 올바른 수령인입니다.\n\n" \
                             f"1. 현황\n" \
                             f" - 수령인 주소: [본인 주소 기재]\n" \
                             f" - 실제 배송 완료 장소: [오배송된 장소/타 동호수 등 기재]\n" \
                             f" - 물품명 및 가액: {item_name_formatted} ({price_formatted})\n\n" \
                             f"2. 청구 사유 및 책임\n" \
                             f" - 본인은 송장에 정확한 주소를 기재하였으나, 귀사 배송기사의 과실로 인해 타인의 주소지에 오배송되었습니다.\n" \
                             f" - 이는 명백한 택배사의 배송 착오 및 계약 불이행입니다. 이에 따라 즉각 오배송된 물품을 수거하여 정상 배송해주실 것을 청구합니다.\n" \
                             f" - 만약 오배송된 물품이 타인에 의해 사용/분실되어 회수가 불가능할 시에는, 상법 제135조 및 택배 약관에 따라 전액 배상({price_formatted}) 처리를 정식 요청합니다.\n\n" \
                             f"3. 추가 조치\n" \
                             f" - 지체 없는 수거 프로세스를 진행해 주시고 결과를 안내해 주시기 바랍니다.\n\n" \
                             f"청구인: [성함]"
        else:
            claim_template = f"제목: 오배송 상품 수령인에 대한 정중한 반환 요청 및 통지서 (내용증명 양식)\n\n" \
                             f"수신인: [오배송지 거주자 또는 관리실]\n" \
                             f"발신인: [본인 성함]\n\n" \
                             f"1. 발송 경위\n" \
                             f" - 발신인의 주소 기재 착오로 인해 귀하의 주소지([오배송 주소])로 발송인 [판매처명]의 택배가 배송 완료되었습니다.\n" \
                             f" - 물품명: {item_name_formatted}\n\n" \
                             f"2. 요청 사항\n" \
                             f" - 해당 물품은 발신인의 착오로 인해 도달한 것으로 귀하의 소유가 아님이 명백합니다.\n" \
                             f" - 이에 본 택배물을 개봉하지 마시고 신속히 반환(수거 협조 또는 연락)해 주시기를 정중히 부탁드립니다.\n\n" \
                             f"3. 법적 참고사항\n" \
                             f" - 만일 잘못 배송된 타인의 물건임을 알고도 이를 반환하지 않고 임의로 개봉하여 사용하거나 처분하는 경우, 대한민국 형법 제360조에 따른 '점유이탈물횡령죄'가 성립되어 처벌을 받을 수 있음을 양지해 주시기 바랍니다.\n" \
                             f" - 원만한 수거와 반환이 조속히 이루어지도록 연락({[본인 연락처]})을 부탁드립니다.\n\n" \
                             f"발신인: [성함]"

        strategies = [
            "**1단계 (택배 기사 신속 연락)**: 오배송 사실을 인지한 즉시 담당 기사에게 전화를 걸어 오배송 사실을 알리고 회수를 요청하십시오. 기사가 직접 수거해서 원주소지로 전달하는 것이 가장 신속한 해결책입니다.",
            "**2단계 (오배송지 접촉 자제)**: 본인이 직접 다른 집(특히 이웃 세대) 문 앞 물건을 무단으로 가져오는 행위는 절도나 주거침입 시비가 붙을 수 있습니다. 반드시 배송 기사나 택배사 공식 프로세스를 통해 수거하게 해야 법적으로 안전합니다.",
            "**3단계 (점유이탈물횡령죄 고지)**: 주소 오입력 등으로 타인이 물건을 수령했는데 반환을 거부할 경우, 해당인에게 형사상 '점유이탈물횡령' 혐의에 처해질 수 있음을 안내하고(내용증명 또는 문자) 합의를 보지 못하면 경찰서에 신고 절차를 밟을 수 있음을 알리십시오."
        ]

    # Structure final response dict
    res_dict = {
        "responsibility": {
            "courier": res_courier,
            "seller": res_seller,
            "buyer": res_buyer
        },
        "analysis": analysis_text,
        "regulations": regulations,
        "claim": claim_template,
        "strategies": strategies
    }
    return res_dict

# ----------------- Gemini API Mode -----------------
def analyze_dispute_with_gemini(api_key, purchase_type, dispute_type, details, item_name, item_price, courier_company, tracking_number, user_story):
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        prompt = f"""
        당신은 대한민국 '택배 분쟁 전문 변호사이자 소비자 권익 보호 전문가'입니다.
        사용자가 택배 분쟁 피해 상황을 호소하고 있습니다.
        제공된 입력 정보와 법률 조항(상법 제135조, 공정위 택배표준약관, 전자상거래법 제13조 등)을 기반으로 전문적이고 사용자 편에서 가장 유리한 대처 방안을 보고서 형식으로 생성해 주세요.

        [입력 정보]
        - 상품 구매처: {purchase_type}
        - 분쟁 유형: {dispute_type}
        - 세부 상황 데이터: {json.dumps(details, ensure_ascii=False)}
        - 물품명: {item_name if item_name else '미지정'}
        - 물품 가액: {item_price:,}원
        - 택배사: {courier_company}
        - 운송장번호: {tracking_number if tracking_number else '미지정'}
        - 사용자 서술 상황: {user_story}

        [출력 요구 사항]
        항상 한국어로 작성하고 실용적이며 가독성이 우수해야 합니다.
        다음 세 가지 항목을 명확하게 구분하여 구체적으로 적어주세요.

        1. **상황 분석 (누구 책임인가?)**
           - 택배사, 판매자, 구매자 세 주체의 구체적인 책임 비율(%)과 그 법적 논리(상법, 민법, 약관 근거 포함)를 상세하게 설명하세요.
           - 관련 소비자 보호 규정을 정밀하게 조망하세요.
        
        2. **고객센터 클레임 문구 (복사/붙여넣기용)**
           - 수신처(쇼핑몰 또는 택배사)에 적합하게 작성하세요.
           - 정중하고 격식 있으나 법리적 책임을 명확히 적어 단호한 어조로 보상(환불/재발송) 청구 내용을 완성하세요.
           - 실제 수치(물품명, 가액 등)가 대입된 최종 완성본으로 바로 쓸 수 있게 하세요.

        3. **환불/보상 전략 (3단계 대응법)**
           - 1단계: 고객센터 및 서면 이의제기 접수 노하우 및 기한 주의사항
           - 2단계: 추가 압박 및 신고 접수(예: 국민신문고, 지자체 교통과 등)
           - 3단계: 최후의 수단 (소비자원 피해구제 접수 및 입증자료 최종 점검)
        """
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API 호출 중 오류가 발생했습니다. 로컬 분석 엔진으로 대체합니다. (오류 내용: {str(e)})"

# Execute analysis on button click
if analyze_btn:
    st.session_state.analyzed = True
    
    if ai_mode and gemini_key:
        with st.spinner("Gemini AI가 정밀 분석 중입니다..."):
            ai_result = analyze_dispute_with_gemini(
                gemini_key, purchase_type, dispute_type, details, 
                item_name, item_price, courier_company, tracking_number, user_story
            )
            # To fit within UI container, parse or display appropriately
            st.session_state.analysis_result = {
                "is_ai": True,
                "raw_text": ai_result
            }
    else:
        with st.spinner("상황 분석 엔진 구동 중..."):
            local_result = analyze_dispute_locally(
                purchase_type, dispute_type, details, 
                item_name, item_price, courier_company, tracking_number, user_story
            )
            st.session_state.analysis_result = {
                "is_ai": False,
                "data": local_result
            }

# Display Results
with col2:
    if st.session_state.analyzed:
        result = st.session_state.analysis_result
        
        st.markdown('<div class="glass-card" style="border-color: rgba(99, 102, 241, 0.5);">', unsafe_allow_html=True)
        st.markdown("## ⚖️ 맞춤형 분쟁 해결 솔루션 리포트")
        st.markdown(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown("---")
        
        if result.get("is_ai"):
            # Show Gemini AI markdown response
            st.markdown(result["raw_text"])
            
            # Text download for AI Report
            st.markdown("---")
            download_text = f"=== 택배 분쟁 AI 정밀 보고서 ===\n생성시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" + result["raw_text"]
            st.markdown(
                get_txt_download_link("택배분쟁_해결_솔루션_리포트.txt", download_text, "📥 분석 보고서 전체 텍스트 다운로드"),
                unsafe_allow_html=True
            )
        else:
            # Show Local rule-engine response
            data = result["data"]
            
            # Tabs for Local Results
            tab1, tab2, tab3 = st.tabs(["📊 1. 상황 분석", "✍️ 2. 클레임 문구", "🚀 3. 환불/보상 전략"])
            
            with tab1:
                st.markdown("### ⚖️ 책임 소재 및 과실 비율 분석")
                
                # Visual responsibility bar
                c_p = data["responsibility"]["courier"]
                s_p = data["responsibility"]["seller"]
                b_p = data["responsibility"]["buyer"]
                
                st.markdown(f"""
                <div style="display: flex; gap: 10px; margin-bottom: 5px;">
                    <span class="badge badge-courier">택배사 귀책: {c_p}%</span>
                    <span class="badge badge-seller">판매자 귀책: {s_p}%</span>
                    <span class="badge badge-buyer">구매자 귀책: {b_p}%</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Progress bar
                st.markdown(f"""
                <div class="responsibility-bar-container">
                    <div class="res-courier" style="width: {c_p}%;">{c_p}% 택배사</div>
                    <div class="res-seller" style="width: {s_p}%;">{s_p}% 판매자</div>
                    <div class="res-buyer" style="width: {b_p}%;">{b_p}% 구매자</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(data["analysis"], unsafe_allow_html=True)
                
                st.markdown("#### 📚 핵심 관련 소비자 규정 및 약관")
                for reg in data["regulations"]:
                    st.markdown(f"- **{reg}**")
            
            with tab2:
                st.markdown("### ✍️ 즉시 발송용 클레임 문구")
                st.caption("아래 텍스트 상자 우측 상단의 복사 버튼을 눌러 바로 활용할 수 있습니다. 괄호([ ]) 쳐진 부분은 자신의 인적사항에 맞춰 기입 후 활용하세요.")
                st.code(data["claim"], language="text")
                
                # Extra Tips for claim
                st.info("💡 **클레임 전달 팁**: 전화를 통한 접수만으로는 구속력이 약할 수 있습니다. 위 문구를 공식 고객센터 이메일이나 1:1 상담 게시판, 혹은 카카오톡 공식 채널 상담원 채팅방으로 보내 서면 자료를 먼저 남기신 후 전화 상담을 진행하십시오.")
            
            with tab3:
                st.markdown("### 🚀 단계별 환불 및 보상 전략 가이드")
                st.markdown("각 단계를 확인하시고 조치를 취해보세요:")
                
                for idx, step in enumerate(data["strategies"]):
                    st.checkbox(step, key=f"step_check_{idx}")
                
                st.markdown("---")
                st.markdown("#### 📞 분쟁 유관 기관 공식 상담 연락처")
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    st.markdown("""
                    - **한국소비자원 (피해구제)**
                      - 전화: 국번없이 1372
                      - 웹사이트: [www.kca.go.kr](https://www.kca.go.kr)
                    """)
                with col_i2:
                    st.markdown("""
                    - **국민신문고 (택배사 위법사항 제보)**
                      - 국토교통부, 공정거래위원회 접수 가능
                      - 웹사이트: [www.epeople.go.kr](https://www.epeople.go.kr)
                    """)
            
            # TXT Download
            st.markdown("---")
            regs_formatted = "\n".join([f"- {r}" for r in data["regulations"]])
            strat_formatted = "\n".join([f"{i+1}. {s}" for i, s in enumerate(data["strategies"])])
            
            download_text = f"""=== 택배 분쟁 해결 전문 솔루션 리포트 ===
생성시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. 상황 분석 및 귀책 비율
- 택배사 과실: {c_p}%
- 판매자 과실: {s_p}%
- 구매자 과실: {b_p}%

[법리 분석]
{data["analysis"].replace('<br>', '\n')}

[관련 규정]
{regs_formatted}

2. 발송용 클레임 전문
------------------------------------------
{data["claim"]}
------------------------------------------

3. 단계별 행동 대응 전략
{strat_formatted}
"""
            st.markdown(
                get_txt_download_link("택배분쟁_해결_솔루션_리포트.txt", download_text, "📥 분석 보고서 전체 텍스트 다운로드"),
                unsafe_allow_html=True
            )
            
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-card" style="text-align: center; padding: 100px 20px;">', unsafe_allow_html=True)
        st.markdown("### 🔍 분석 대기 중")
        st.markdown("왼쪽 입력 폼에 피해 상황 정보를 상세히 입력하신 뒤, **[분쟁 상황 분석 및 솔루션 생성]** 버튼을 누르시면 전문 법률 분석과 맞춤 클레임 문구가 출력됩니다.")
        st.markdown('</div>', unsafe_allow_html=True)
