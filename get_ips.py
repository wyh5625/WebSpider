import requests


# Function to extract IPs and ports from a file
def extract_ips_from_file(file_path):
    ip_ports = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Remove any leading/trailing whitespace
                if line:  # Check if the line is not empty
                    ip, port = line.split(':')
                    ip_ports.append({'ip': ip, 'port': port})
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return ip_ports

if __name__ == "__main__":
    # Specify the path to your txt file
    file_path = 'ip_list.txt'  # Change this to your file path

    # Extracting the IPs and ports
    extracted_ips = extract_ips_from_file(file_path)
    # Printing the result
    for entry in extracted_ips:
        print(entry)




# 获取 IP 地址
# ip_addresses = fetch_ips(api_url)

# 打印提取的 IP 地址
# print("提取的 IP 地址:")
# for ip in ip_addresses:
#     print(ip)