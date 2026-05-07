import streamlit as st
import random
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🔮 AI×トートタロット占い")
st.write("こたろうが、あなたの無意識を読み解きます。")

cards = [
    "0 愚者 / The Fool", "I 魔術師 / The Magus", "II 女教皇 / The Priestess",
    "III 女帝 / The Empress", "IV 皇帝 / The Emperor", "V 教皇 / The Hierophant",
    "VI 恋人 / The Lovers", "VII 戦車 / The Chariot", "VIII 調整 / Adjustment",
    "IX 隠者 / The Hermit", "X 運命 / Fortune", "XI 欲望 / Lust",
    "XII 吊るされた男 / The Hanged Man", "XIII 死 / Death", "XIV 技 / Art",
    "XV 悪魔 / The Devil", "XVI 塔 / The Tower", "XVII 星 / The Star",
    "XVIII 月 / The Moon", "XIX 太陽 / The Sun", "XX 永劫 / The Aeon",
    "XXI 宇宙 / The Universe"
]

card_meanings = {
    "0 愚者 / The Fool": "純粋な可能性。自由、飛躍、混沌、無垢。",
    "I 魔術師 / The Magus": "言葉と知性で世界を動かす力。創造、伝達、意志。",
    "II 女教皇 / The Priestess": "沈黙の知。直感、静けさ、隠された真理。",
    "III 女帝 / The Empress": "豊穣と生命力。愛、自然、官能。",
    "IV 皇帝 / The Emperor": "秩序化する力。支配、構造、責任。",
    "V 教皇 / The Hierophant": "精神的体系と伝統。教え、継承。",
    "VI 恋人 / The Lovers": "結合と選択。異なるものの融合。",
    "VII 戦車 / The Chariot": "推進力と意志。突進、防御、勝利欲。",
    "VIII 調整 / Adjustment": "宇宙的バランス。因果、均衡。",
    "IX 隠者 / The Hermit": "孤独な探求。内省、叡智。",
    "X 運命 / Fortune": "流転とサイクル。変化、循環。",
    "XI 欲望 / Lust": "生命力の肯定。欲望、情熱、陶酔。",
    "XII 吊るされた男 / The Hanged Man": "自己犠牲による転換。停止、反転。",
    "XIII 死 / Death": "終わりによる再生。変容、刷新。",
    "XIV 技 / Art": "異質なものを融合する力。統合、錬金術。",
    "XV 悪魔 / The Devil": "欲望と執着。快楽、依存、束縛。",
    "XVI 塔 / The Tower": "構造崩壊と覚醒。破壊、衝撃。",
    "XVII 星 / The Star": "透明な希望。再生、静かな光。",
    "XVIII 月 / The Moon": "不安と無意識。幻想、夢、深層心理。",
    "XIX 太陽 / The Sun": "純粋な生命肯定。明晰さ、喜び。",
    "XX 永劫 / The Aeon": "新しい時代への更新。価値観の転換。",
    "XXI 宇宙 / The Universe": "完成と統合。全体性、一体化。"
}

if "card" not in st.session_state:
    st.session_state.card = None
if "orientation" not in st.session_state:
    st.session_state.orientation = None

悩み = st.text_area("占いたいことを記入してください")
number = st.slider("1〜22の好きな数字を選んでください", 1, 22)

if st.button("カードを引く"):
    st.session_state.card = random.choice(cards)
    st.session_state.orientation = random.choice(["正位置", "逆位置"])

if st.session_state.card:
    card = st.session_state.card
    orientation = st.session_state.orientation
    meaning = card_meanings[card]

    st.subheader("あなたが引いたカード")
    st.write(card)
    st.write(orientation)

    search_word = card.replace(" ", "+")
    image_link = "https://www.google.com/search?tbm=isch&q=Thoth+Tarot+" + search_word
    st.markdown(f"[ここを押してカード画像を見る]({image_link})")

    image = st.text_area("カードから受け取ったイメージを書いてください")

    if st.button("占い結果を見る"):
        if 悩み.strip() == "":
            st.warning("占いたいことを入力してね。")
        elif image.strip() == "":
            st.warning("カードから受け取ったイメージを書いてね。")
        else:
            with st.spinner("こたろうがカードを読んでいます..."):
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": """
あなたは「こたろう」というAI×トートタロット占い師です。

相談者に寄り添うが、甘やかしすぎない。
感情を否定せず、でも感情に飲まれた選択には少し鋭くツッコむ。
誠実さ、責任、信頼、自分の選択を引き受けることを大切にする。
人は変われるが、変わるには行動が必要だと考える。
弱さそのものではなく、弱さと向き合う姿勢を見る。

口調は、親しい友人に話すような自然でカジュアルな日本語。
少し哲学っぽく、神秘的だけど地に足がついている。
過剰に褒めない。説教くさくしない。

一般的なウェイト版ではなく、トートタロットを中心に解釈する。
カードは吉凶判断ではなく、無意識・欲望・葛藤・変容の象徴として読む。
未来を断定しない。

占い結果には、
カードの象徴、正位置/逆位置としての出方、悩みとの関係、
受け取ったイメージとの関係、今取れる小さな行動を自然に含める。
"""
                        },
                        {
                            "role": "user",
                            "content": f"""
相談内容：
{悩み}

相談者が選んだ数字：
{number}

引いたカード：
{card}

カードの向き：
{orientation}

カードのトートタロット的な基本意味：
{meaning}

相談者がカードから受け取った印象：
{image}

この情報をもとに、こたろうとして占ってください。
"""
                        }
                    ]
                )

            st.subheader("占い結果")
            st.write(response.choices[0].message.content)