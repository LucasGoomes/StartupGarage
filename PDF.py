from fpdf import FPDF  

class PDF(FPDF):  
        def header(self):  
            # Arial bold 12  
            self.set_font('Arial', 'B', 12)  
            # Title  
            self.cell(0, 10, 'Letter of Intent', 0, 1, 'C')  
  
        def footer(self):  
            # Go to 1.5 cm from bottom  
            self.set_y(-15)  
            # Arial italic 8  
            self.set_font('Arial', 'I', 8)  
            # Page number  
            self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C') 