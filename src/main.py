from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from output_tabs import OutputTabs
from input_tabs import InputTabs
from request_bar import RequestBar
from utils import parse_json_body
import sys, requests, json

class HttpClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Python Requests")
        self.setGeometry(100, 100, 1200, 800)
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.request_bar = RequestBar()
        main_layout.addLayout(self.request_bar)
        self.input_tab_widget = InputTabs()
        main_layout.addWidget(self.input_tab_widget)
        self.output_tab_widget = OutputTabs()
        main_layout.addWidget(self.output_tab_widget)
        self.setCentralWidget(main_widget)
        # Connect signals
        self.request_bar.send_button.clicked.connect(self.send_request)
        self.request_bar.url_input.returnPressed.connect(self.send_request)        
    
    def send_request(self):
        current_url = self.request_bar.url_input.text()
        if current_url.replace("http://", "").replace("https://", "") != "":
            try:
                method = self.request_bar.http_verb.currentText()
                url = self.request_bar.url_input.text()
                headers = self.input_tab_widget.get_headers()
                params = self.input_tab_widget.get_params()
                data = self.input_tab_widget.get_body()
                if data:
                    try:
                        data_dict = parse_json_body(data)
                        if isinstance(data_dict, str):
                            self.output_tab_widget.response_text.setText(data_dict)
                            return
                    except Exception as e:
                        self.output_tab_widget.response_text.setText(f"Error parsing JSON: {str(e)}")
                        return
                else:
                    data_dict = None
                r = requests.request(method, url, headers=headers, params=params, json=data_dict)
                formatted_headers = self.format_headers(r.headers)
                self.output_tab_widget.headers_text.setText(formatted_headers)
                formatted_response = self.format_response(r)
                self.output_tab_widget.response_text.setText(formatted_response)
            except requests.RequestException as e:
                self.output_tab_widget.response_text.setText(f"Error sending request: {str(e)}")
        else:
            return self.output_tab_widget.response_text.setText("Could not send request")
            # dummyjson.com/test
            
    def format_headers(self, headers):
        return "\n".join([f"{k}: {v}" for k, v in headers.items()])
    
    def format_response(self, response):
        try:
            json_data = response.json()
            return json.dumps(json_data, indent=2)
        except ValueError:
            return response.text

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HttpClientWindow()
    window.show()
    sys.exit(app.exec())