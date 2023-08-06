import json
import os
import sys
from datetime import datetime

import pandas as pd
import requests
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QFileDialog, QProgressDialog, QTextEdit


class WebListInfoSpider(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # 设置窗口属性
        self.setWindowTitle('通用网页列表信息抓取工具')
        # 初始化布局
        layout = QVBoxLayout()
        # 设置layout为横向布局
        layout.setDirection(QVBoxLayout.LeftToRight)
        output_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        # input和output布局各占50%
        output_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(input_layout, 1)
        layout.addLayout(output_layout, 1)

        # 创建输入框及标签
        self.url_input = QLineEdit(self)
        self.method_input = QLineEdit(self)
        self.pagination_param_name_input = QLineEdit(self)
        self.pagination_size_param_name_input = QLineEdit(self)
        self.start_page_input = QLineEdit(self)
        self.max_page_input = QLineEdit(self)
        self.page_size = QLineEdit(self)
        self.extra_params_input = QLineEdit(self)
        self.other_headers = QLineEdit(self)
        self.token_input = QLineEdit(self)
        self.json_path_input = QLineEdit(self)

        # 添加组件到布局
        input_layout.addWidget(QLabel('URL*:'))
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(QLabel('请求方法*:'))
        input_layout.addWidget(self.method_input)
        input_layout.addWidget(QLabel('page参数字段名称*:'))
        input_layout.addWidget(self.pagination_param_name_input)
        input_layout.addWidget(QLabel('pageSize参数字段名称*:'))
        input_layout.addWidget(self.pagination_size_param_name_input)
        input_layout.addWidget(QLabel('起始页数*:'))
        input_layout.addWidget(self.start_page_input)
        input_layout.addWidget(QLabel('最大页数*:'))
        input_layout.addWidget(self.max_page_input)
        input_layout.addWidget(QLabel('每页大小*:'))
        input_layout.addWidget(self.page_size)
        input_layout.addWidget(QLabel('额外参数:'))
        input_layout.addWidget(self.extra_params_input)
        input_layout.addWidget(QLabel('其他请求头:'))
        input_layout.addWidget(self.other_headers)
        input_layout.addWidget(QLabel('认证Token:'))
        input_layout.addWidget(self.token_input)
        input_layout.addWidget(QLabel('JSON返回值的列表字段属性路径*:'))
        input_layout.addWidget(self.json_path_input)

        self.read_button = QPushButton('读取抓取指令', self)
        self.read_button.clicked.connect(self.read_command)
        input_layout.addWidget(self.read_button)

        self.export_button = QPushButton('导出抓取指令', self)
        self.export_button.clicked.connect(self.export_command)
        input_layout.addWidget(self.export_button)

        # 创建按钮
        self.scrape_button = QPushButton('开始抓取', self)
        self.scrape_button.clicked.connect(self.scrape)
        input_layout.addWidget(self.scrape_button)

        # output_layout设置一个文本显示区域，可以滚动,铺满整个output_layout 用于输出抓取结果
        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        # 设置最大宽度
        self.output.setMaximumWidth(600)
        self.output.setAlignment(Qt.AlignTop)
        self.output.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.output.setText('运行日志:')
        # 边框设置线条宽度为2px
        # self.output.setFrameShape(QLabel.Box)
        self.output.setFrameShadow(QLabel.Sunken)
        output_layout.addWidget(self.output, 9)

        self.export_log_button = QPushButton('导出日志', self)
        self.export_log_button.clicked.connect(self.export_log)
        output_layout.addWidget(self.export_log_button, 1)

        # 设置窗口布局
        self.setLayout(layout)

    def export_log(self):
        # 弹窗选择导出路径
        file_path, _ = QFileDialog.getSaveFileName(self, '导出日志', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.output.toPlainText())

    def log(self, text):
        self.output.append(text)

    # 读取抓取指令
    def read_command(self):
        # 弹窗选择JSON文件
        file_path, _ = QFileDialog.getOpenFileName(self, '选择JSON文件', '', 'JSON Files (*.json)')
        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
            self.url_input.setText(data.get('url'))
            self.method_input.setText(data.get('method'))
            self.pagination_param_name_input.setText(data.get('pagination_param_name'))
            self.pagination_size_param_name_input.setText(data.get('pagination_size_param_name'))
            self.start_page_input.setText(data.get('start_page'))
            self.max_page_input.setText(data.get('max_page'))
            self.page_size.setText(data.get('page_size'))
            self.extra_params_input.setText(data.get('extra_params'))
            self.other_headers.setText(data.get('other_headers'))
            self.token_input.setText(data.get('token'))
            self.json_path_input.setText(data.get('json_path'))

    # 导出抓取指令
    def export_command(self):
        # 弹窗选择导出路径
        file_path, _ = QFileDialog.getSaveFileName(self, '导出JSON文件', '', 'JSON Files (*.json)')
        if file_path:
            data = {
                'url': self.url_input.text(),
                'method': self.method_input.text(),
                'pagination_param_name': self.pagination_param_name_input.text(),
                'pagination_size_param_name': self.pagination_size_param_name_input.text(),
                'start_page': self.start_page_input.text(),
                'max_page': self.max_page_input.text(),
                'page_size': self.page_size.text(),
                'extra_params': self.extra_params_input.text(),
                'other_headers': self.other_headers.text(),
                'token': self.token_input.text(),
                'json_path': self.json_path_input.text()
            }
            with open(file_path, 'w') as file:
                json.dump(data, file)
            QMessageBox.information(self, '导出成功', '导出成功', QMessageBox.Ok)

    def scrape(self):
        url = self.url_input.text().strip()
        method = self.method_input.text().strip()
        pagination_param_name = self.pagination_param_name_input.text().strip()
        pagination_size_param_name = self.pagination_size_param_name_input.text().strip()
        start_page = int(self.start_page_input.text().strip())
        max_page = int(self.max_page_input.text().strip())
        page_size = int(self.page_size.text().strip())
        extra_params = self.extra_params_input.text().strip() or '{}'
        other_headers = self.other_headers.text().strip() or '{}'
        token = self.token_input.text()
        json_path = self.json_path_input.text().split('.')

        self.log(f"==> 开始执行爬取任务")
        self.log(f"==> 请求地址: {url}")
        self.log(f"==> 请求方式: {method}")
        self.log(f"==> 分页参数名: {pagination_param_name}")
        self.log(f"==> 分页大小参数名: {pagination_size_param_name}")
        self.log(f"==> 起始页: {start_page}")
        self.log(f"==> 最大页: {max_page}")
        self.log(f"==> 分页大小: {page_size}")
        self.log(f"==> 额外参数: {extra_params}")
        self.log(f"==> 其他请求头: {other_headers}")
        self.log(f"==> Token: {token}")
        self.log(f"==> JSON路径: {json_path}")

        try:
            extra_params = json.loads(extra_params)
        except:
            QMessageBox.warning(self, '额外参数格式错误', '额外参数格式错误', QMessageBox.Ok)
            return

        headers = {'Cookie': token}
        try:
            other_headers = json.loads(other_headers)
            headers.update(other_headers)
        except:
            QMessageBox.warning(self, '其他请求头格式错误', '其他请求头格式错误', QMessageBox.Ok)
            return

        results = []

        progress = QProgressDialog('正在抓取第{}/{}页'.format(0, max_page), '取消', 0, max_page - start_page + 1, self)
        progress.setWindowTitle('抓取进度')
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        for page in range(start_page, max_page + 1):
            # 弹出进度条
            progress.setValue(page - start_page + 1)
            progress.setLabelText('正在抓取第{}/{}页'.format(page, max_page))
            self.log(f" -> 正在抓取第{page}/{max_page}页")
            # 如果progress取消，则break
            if progress.wasCanceled():
                progress.close()
                self.log(f"==> 爬取任务被取消")
                break

            params = {
                pagination_param_name: page,
                pagination_size_param_name: page_size,
                **extra_params
            }

            try:
                if method == 'GET':
                    response = requests.get(url, headers=headers, params=params)
                elif method == 'POST':
                    response = requests.post(url, headers=headers, json=params)
                else:
                    response = requests.request(method, url, headers=headers, params=params)

                if response.status_code != 200:
                    raise Exception(f"请求失败，状态码: {response.status_code}")

                data = response.json()

                if not data:
                    raise Exception(f"返回数据为空")

                for key in json_path:
                    data = data[key]

                results.extend(data)
                self.log(f" -> 第{page}页抓取成功")
                self.log(f" -> 第{page}页数据共计: {len(data)}条")
                self.log(f" -> 第{page}页数据已添加到结果中, 当前已爬取数据总计: {len(results)}条")

            except Exception as e:
                self.log(f" -> 第{page}页抓取失败: {str(e)}")
                # 弹窗提示请求错误，让用户确认是否继续
                reply = QMessageBox.warning(self, '请求错误', '请求错误，是否继续？', QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    self.log(f"==> 爬取任务被取消, 已抓取到第{page}页")
                    return

        progress.close()
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        output_excel = f"{timestamp}.xlsx"
        df = pd.DataFrame(results)
        df.to_excel(output_excel, index=False)

        self.log(f"==> 爬取任务完成")
        # 弹窗提示
        QMessageBox.information(self, '信息', f"抓取完成，已导出至 {output_excel}")

        # 打开文件所在路径
        os.system(f"open {os.path.dirname(os.path.realpath(output_excel))}")


def cli():
    app = QApplication(sys.argv)
    scraper = WebListInfoSpider()
    scraper.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    cli()
