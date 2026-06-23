import argparse
import random
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

def generate_64masu_pdf(filename, operator='+', min_val=10, max_val=99):
    c = canvas.Canvas(filename, pagesize=A4)
    # 日本語フォントの登録 (標準で使えるHeiseiKakuGo-W5を使用)
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
    
    # 問題の数値を生成
    top_nums = [random.randint(min_val, max_val) for _ in range(8)]
    left_nums = [random.randint(min_val, max_val) for _ in range(8)]
    
    # 引き算の場合、答えがマイナスにならないように左の数値を大きくする調整
    if operator == '-':
        left_nums = [random.randint(max_val, max_val + 50) for _ in range(8)]
        top_nums = [random.randint(min_val, max_val) for _ in range(8)]
    
    def draw_page(is_answer=False):
        # タイトル
        c.setFont('HeiseiKakuGo-W5', 24)
        title_op = "足し算" if operator == '+' else "引き算" if operator == '-' else "掛け算"
        title = f"64ます計算 ({title_op}) {' - 解答' if is_answer else ''}"
        c.drawString(70, 780, title)
        
        # 日付・名前欄
        c.setFont('HeiseiKakuGo-W5', 14)
        c.drawString(350, 780, "年　　月　　日")
        c.drawString(350, 750, "名前：")
        
        c.setFont('Helvetica', 18)
        
        cell_size = 50
        start_x = 72
        start_y = 700
        
        # グリッドの描画
        c.setLineWidth(1)
        for i in range(10):
            # 水平線
            y = start_y - i * cell_size
            c.line(start_x, y, start_x + 9 * cell_size, y)
            # 垂直線
            x = start_x + i * cell_size
            c.line(x, start_y, x, start_y - 9 * cell_size)
            
        # 太線で外枠と見出し行・列を強調
        c.setLineWidth(2)
        c.rect(start_x, start_y - 9 * cell_size, 9 * cell_size, 9 * cell_size)
        c.line(start_x, start_y - cell_size, start_x + 9 * cell_size, start_y - cell_size)
        c.line(start_x + cell_size, start_y, start_x + cell_size, start_y - 9 * cell_size)
            
        # 演算子の描画
        c.setFont('Helvetica-Bold', 24)
        c.drawCentredString(start_x + cell_size/2, start_y - cell_size/2 - 8, operator)
        
        # 上部の数値を描画
        c.setFont('Helvetica-Bold', 20)
        for i, num in enumerate(top_nums):
            c.drawCentredString(start_x + (i+1.5)*cell_size, start_y - cell_size/2 - 7, str(num))
            
        # 左側の数値を描画
        for i, num in enumerate(left_nums):
            c.drawCentredString(start_x + cell_size/2, start_y - (i+1.5)*cell_size - 7, str(num))
            
        # 解答の描画
        if is_answer:
            c.setFont('Helvetica', 18)
            for row, l_num in enumerate(left_nums):
                for col, t_num in enumerate(top_nums):
                    if operator == '+':
                        ans = l_num + t_num
                    elif operator == '-':
                        ans = l_num - t_num
                    elif operator == 'x' or operator == '*':
                        ans = l_num * t_num
                    
                    # 答えをセルの中央に配置
                    c.drawCentredString(start_x + (col+1.5)*cell_size, start_y - (row+1.5)*cell_size - 6, str(ans))
                    
        c.showPage()

    # 問題ページ
    draw_page(is_answer=False)
    # 解答ページ
    draw_page(is_answer=True)
    
    c.save()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='64ます計算のPDFを生成します。')
    parser.add_argument('-o', '--operator', type=str, default='+', choices=['+', '-', 'x'], help='計算の種類 (+, -, x)')
    parser.add_argument('-min', '--min_val', type=int, default=10, help='最小値 (デフォルト: 10)')
    parser.add_argument('-max', '--max_val', type=int, default=99, help='最大値 (デフォルト: 99)')
    
    args = parser.parse_args()
    
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    op_name = "add" if args.operator == '+' else "sub" if args.operator == '-' else "mul"
    filename = f"64masu_{op_name}_{date_str}.pdf"
    
    generate_64masu_pdf(filename, operator=args.operator, min_val=args.min_val, max_val=args.max_val)
    print(f"PDFを作成しました: {filename}")
