import streamlit as st
import random
import pandas as pd

# ページ設定
st.set_page_config(page_title="実習G ペア作成", layout="centered")

st.title("🧪 実習G：ペア作成システム")
st.markdown("学籍番号を貼り付けてボタンを押してください。ペア内で番号が小さい順に自動整列します。")

# 入力エリア
input_data = st.text_area("学籍番号を入力（改行区切り）", placeholder="24001\n24002\n24003...", height=200)

# サイドバー設定
st.sidebar.header("設定")
odd_handling = st.sidebar.radio("人数が奇数の場合：", ["最後の組を3人にする", "1人を「余り」にする"])

if st.button("ランダムペアを生成"):
    # データ整形（空行削除）
    students = [line.strip() for line in input_data.split('\n') if line.strip()]
    
    if len(students) < 2:
        st.warning("学生を2人以上入力してください。")
    else:
        # 1. まず全体をシャッフル
        random.shuffle(students)
        
        pairs = []
        # 2. ペアを作成し、その中でソートする
        while len(students) >= 2:
            # 3人組にする設定で、残りが3人の場合
            if len(students) == 3 and odd_handling == "最後の組を3人にする":
                p = [students.pop(0), students.pop(0), students.pop(0)]
                p.sort() # 3人を昇順に
                pairs.append(p)
            else:
                p = [students.pop(0), students.pop(0)]
                p.sort() # 2人を昇順に
                pairs.append(p)
        
        # 1人余る設定の場合
        if students:
            pairs.append([students.pop(0), "（余り）"])

        # 3. 結果を表示用にデータフレーム化
        result_data = []
        for i, p in enumerate(pairs):
            row = {
                "グループ": f"第{i+1}組",
                "メンバー1": p[0],
                "メンバー2": p[1] if len(p) > 1 else "",
            }
            if any(len(x) > 2 for x in pairs): # 3人組が存在する場合のみ列を追加
                row["メンバー3"] = p[2] if len(p) > 2 else ""
            result_data.append(row)
        
        df_result = pd.DataFrame(result_data)
        
        st.subheader("生成結果")
        st.table(df_result)

        # 4. CSVダウンロード（BOM付きUTF-8でExcel文字化け防止）
        csv = df_result.to_csv(index=False).encode('utf_8_sig')
        
        st.download_button(
            label="✅ 結果をCSVでダウンロード（Excel対応）",
            data=csv,
            file_name='jisshu_g_pairs.csv',
            mime='text/csv',
        )

st.info("※入力されたデータはブラウザを閉じると消去されます。外部サーバーには保存されません。")