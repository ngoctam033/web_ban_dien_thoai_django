import psycopg2
import datetime
class Database:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()

    def execute(self, query):
        self.cur.execute(query)

    def fetchall(self):
        return self.cur.fetchall()

    def commit(self):
        self.conn.commit()

    #tạo một hàm để thay thế một cột trong sql

    def fetchone(self):
        #tạo một biến để lưu mảng của fetchall
        result = self.fetchall()
        #tạo một cặp key-value mỗi hãng điện thoại tương ứng với 2 chữ số
        dict = {
            'iPhone': 23,
            'Samsung': 24,
            'Xiaomi': 25,
            'OPPO': 26,
            'Vivo': 27,
            'Realme': 28,
            'realme':28,
            'Nokia': 29,
            'Huawei': 30,
            'Masstel': 31,
            'Honor': 32,
            'ViVo': 33,
        }
        #tạo một vòng lặp để duyẹt qua mảng
        b=1000
        for row in result:
            print(row)
            #tạo một mảng, mối phần tử có 2 chữ số
            a = [23]
            split_array = []
            #tách từng từ trong row
            split_array = row[0].split()
            #duyệt qua mảng split_array
            if split_array[0] in dict:
                #nếu i nằm trong dict thì thêm giá trị của i vào mảng a
                a.append(dict[split_array[0]])
                a.append(b)
                b+=1
            #nối mảng a thành một số
            c = int(''.join(map(str, a)))
            #tạo câu truy vấn để import c vào cột product_id, nếu không thưc hiện được thì báo lỗi
            try:
                self.execute(f"UPDATE product SET product_id = {c} WHERE name = '{row[0]}'")
            except:
                print(f"UPDATE product SET product_id = {c} WHERE name = '{row[0]}'")
                print('Error')
    

    def close(self):
        self.conn.close()
        self.cur.close()
        print('Connection closed')

def generate_order_id():
        # Get the current date
        current_date = datetime.date.today()
        # Format the date and append a 4-digit sequence
        order_id = current_date.strftime('%d%m%Y')
        return order_id
if __name__ == '__main__':
    #db = Database('CDTT2', 'postgres', '0303', 'localhost', '5432')
    #db.execute('SELECT * FROM product')
    #db.fetchone()
    #print(db.fetchall())
    #db.commit()
    #db.close()
    print(generate_order_id())