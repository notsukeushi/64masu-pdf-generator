import argparse
import random
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# A4 size in points
PAGE_WIDTH, PAGE_HEIGHT = A4

# Grid layout parameters
MARGIN_LEFT = 42.52
CELL_W = 56.69
CELL_H = 34.01

GRID1_Y_START = PAGE_HEIGHT - 86.69
GRID2_Y_START = PAGE_HEIGHT - 421.18

def draw_grid(c, x_start, y_start, operator, top_nums, left_nums, is_answer=False):
    # Draw grid lines
    c.setLineWidth(1)
    for i in range(10):
        # Horizontal lines
        y = y_start - i * CELL_H
        c.line(x_start, y, x_start + 9 * CELL_W, y)
        # Vertical lines
        x = x_start + i * CELL_W
        c.line(x, y_start, x, y_start - 9 * CELL_H)
        
    # Draw thick borders
    c.setLineWidth(2)
    c.rect(x_start, y_start - 9 * CELL_H, 9 * CELL_W, 9 * CELL_H)
    c.line(x_start, y_start - CELL_H, x_start + 9 * CELL_W, y_start - CELL_H)
    c.line(x_start + CELL_W, y_start, x_start + CELL_W, y_start - 9 * CELL_H)
    
    # Draw operator
    c.setFont('HeiseiMin-W3', 18)
    # Adjust position to center
    c.drawCentredString(x_start + CELL_W / 2, y_start - CELL_H / 2 - 6, operator)
    
    # Draw top numbers
    c.setFont('Helvetica', 18)
    for i, num in enumerate(top_nums):
        c.drawCentredString(x_start + (i + 1.5) * CELL_W, y_start - CELL_H / 2 - 6, str(num))
        
    # Draw left numbers
    for i, num in enumerate(left_nums):
        c.drawCentredString(x_start + CELL_W / 2, y_start - (i + 1.5) * CELL_H - 6, str(num))
        
    # Draw answers if needed
    if is_answer:
        c.setFont('Helvetica', 18)
        for row, l_num in enumerate(left_nums):
            for col, t_num in enumerate(top_nums):
                if operator == '＋':
                    ans = l_num + t_num
                elif operator == '－':
                    ans = l_num - t_num
                c.drawCentredString(x_start + (col + 1.5) * CELL_W, y_start - (row + 1.5) * CELL_H - 6, str(ans))

def generate_pdf(filename, num_sets=8):
    c = canvas.Canvas(filename, pagesize=A4)
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
    
    for set_idx in range(1, num_sets + 1):
        # Generate numbers for this set
        # Addition: top 1 digit (2-9), left 2 digits (11-19)
        add_top = [random.randint(2, 9) for _ in range(8)]
        add_left = [random.randint(11, 19) for _ in range(8)]
        
        # Subtraction: top 1 digit (2-9), left 2 digits (11-19)
        sub_top = [random.randint(2, 9) for _ in range(8)]
        sub_left = [random.randint(11, 19) for _ in range(8)]
        
        for is_answer in [False, True]:
            # Draw title
            c.setFont('HeiseiMin-W3', 14)
            if is_answer:
                title = f"第{set_idx}セット（教師用・解答付き）"
            else:
                title = f"第{set_idx}セット（生徒用）"
            
            # Title position: x=62.69, y=841.89-66.01=775.88
            c.drawString(62.69, PAGE_HEIGHT - 66.01, title)
            
            # Draw Grid 1 (Addition)
            draw_grid(c, MARGIN_LEFT, GRID1_Y_START, '＋', add_top, add_left, is_answer)
            
            # Draw Grid 2 (Subtraction)
            draw_grid(c, MARGIN_LEFT, GRID2_Y_START, '－', sub_top, sub_left, is_answer)
            
            c.showPage()
            
    c.save()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='64ます計算のPDFを生成します（2桁足し算・引き算形式）')
    parser.add_argument('-n', '--num_sets', type=int, default=8, help='生成するセット数（デフォルト: 8）')
    args = parser.parse_args()
    
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"64masu_add_sub_8sets_{date_str}.pdf"
    
    generate_pdf(filename, num_sets=args.num_sets)
    print(f"PDFを作成しました: {filename}")
