import os

def replace_slashes_in_directory(target_dir=".", allowed_extensions=None):
    """
    遍历目录替换 "//" 为 "\\"，保持原编码不变。
    
    :param target_dir: 目标目录，默认为当前目录
    :param allowed_extensions: 允许处理的文件后缀元组，如 ('.txt', '.py')。如果为 None 则处理所有文件。
    """
    # 在二进制模式下，'//' 表示为 b'//'
    # '\\' 需要转义，所以两个反斜杠在 Python 字节串中写作 b'\\\\'
    search_pattern = b"\\\\"
    replace_pattern = b"\"//"
    
    updated_count = 0
    error_count = 0

    print(f"开始扫描目录: {os.path.abspath(target_dir)}")

    for root, dirs, files in os.walk(target_dir):
        # 忽略 .git 或 .svn 等隐藏版本控制目录（可选，但强烈建议）
        if '.git' in dirs:
            dirs.remove('.git')

        for file_name in files:
            # 扩展名安全检查
            if allowed_extensions and not file_name.endswith(allowed_extensions):
                continue
                
            file_path = os.path.join(root, file_name)
            
            try:
                # 1. 以二进制只读模式打开文件
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                # 2. 如果找到了匹配的字节序列才进行写入操作
                if search_pattern in content:
                    new_content = content.replace(search_pattern, replace_pattern)
                    
                    # 3. 以二进制写入模式覆盖原文件
                    with open(file_path, 'wb') as f:
                        f.write(new_content)
                        
                    print(f"[成功修改] {file_path}")
                    updated_count += 1
                    
            except Exception as e:
                print(f"[读取/写入错误] {file_path}: {e}")
                error_count += 1

    print("-" * 30)
    print(f"处理完成！共修改了 {updated_count} 个文件，遇到 {error_count} 个错误。")

if __name__ == "__main__":
    # 【强烈建议】在此处定义你想要修改的文件类型，防止破坏二进制文件
    # 例如：safe_extensions = ('.txt', '.py', '.json', '.md', '.c', '.cpp', '.h', '.js')
    # 如果确定目标目录里全是纯文本文件，可以将其设为 None
    safe_extensions = ('.html') 
    
    # 获取当前脚本所在目录
    current_directory = os.getcwd()
    
    # 运行替换函数
    replace_slashes_in_directory(current_directory, allowed_extensions=safe_extensions)
