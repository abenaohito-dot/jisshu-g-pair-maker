import streamlit as st
import random
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="実習G ペア作成", layout="centered")

st.title("🧪 実習G：ペア作成システム")
st.markdown("学籍番号を貼り付けてボタンを押してください。")

# 入力エリア
input_data = st.text_area("学籍番号を入力（改行区切り）", placeholder="24001\n24002\n24003...", height=200)

# サイドバー設定
st.sidebar.header("設定")
odd_handling = st.sidebar.radio("人数が奇数の場合：", ["最後の組を3人にする", "1人を「余り」にする"])

if st.button("ランダムペアを生成"):
    # データ整形
    students = [line.strip() for line in input_data.split('\n') if line.strip()]
    
    if len(students) < 2:
        st.warning("学生を2人以上入力してください。")
    else:
        # シャッフル
        random.shuffle(students)
        
        pairs = []
        # 奇数対応：3人組にする場合
        if len(students) % 2 != 0 and odd_handling == "最後の組を3人にする":
            while len(students) > 3:
                pairs.append([students.pop(0), students.pop(0)])
            pairs.append(students) # 残りの3人をひとまとめ
        else:
            # 通常のペア作成
            while len(students) >= 2:
                pairs.append([students.pop(0), students.pop(0)])
            # 1人余りの場合
            if students:
                pairs.append([students.pop(0), "（余り）"])

        # 結果をデータフレーム化
        result_data = []
        for i, p in enumerate(pairs):
            result_data.append({
                "グループ": f"第{i+1}組",
                "メンバー1": p[0],
                "メンバー2": p[1] if len(p) > 1 else "",
                "メンバー3": p[2] if len(p) > 2 else ""
            })
        
        df_result = pd.DataFrame(result_data)
        
        st.subheader("生成結果")
        st.table(df_result)

        # CSVの準備（Excelでそのまま開けるように設定）
        # encoding='utf_8_sig' がExcelの文字化けを防ぐポイントです
        csv = df_result.to_csv(index=False).encode('utf_8_sig')
        
        st.download_button(
            label="✅ 結果をCSVでダウンロード",
            data=csv,
            file_name='jisshu_g_pairs.csv',
            mime='text/csv',
        )

st.info("※ブラウザの再読み込みをすると入力データはクリアされます。")