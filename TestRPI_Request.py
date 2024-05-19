import requests
import threading

url_get_waste_machine_profile = "https://books-opening.gl.at.ply.gg:61345/api/v1/weightScale/machine/all"
url_get_waste_profile = "https://books-opening.gl.at.ply.gg:61345/api/v1/weightScale/profile_of_waste/all"
url_get_waste_history = "https://books-opening.gl.at.ply.gg:61345/api/v1/weightScale/record/all"
url_post_data = 'https://books-opening.gl.at.ply.gg:61345/api/v1/weightScale/record/add'

# !---------------------------------------------------------------< get machine profile >
def get_all_machine_profile():
    try:
        response = requests.get(url_get_waste_machine_profile , verify=False)
        if response.status_code == 200:
                print("Request successful!")
                response_json = response.json()
                print("Response machine profile: " + str(response_json))
                return response_json
        else:
            print("Request profile: failed with status code:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("POST request failed:", e)
        return None

# !---------------------------------------------------------------< get โปรไฟล์ขยะ >
def get_waste_profile():
    try:
        response = requests.get(url_get_waste_profile , verify=False)
        if response.status_code == 200:
                print("Request successful!")
                response_json = response.json()
                print("Response profile: " + str(response_json))
                # Handle response data here
        else:
            print("Request profile: failed with status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("POST request failed:", e)

# !---------------------------------------------------------------< get ประวัติการทิ้ง >
def get_history():
    try:
        response = requests.get(url_get_waste_history, verify=False)
        if response.status_code == 200:
                print("Request successful!")
                response_json = response.json()
                print("Response history: " + str(response_json))
                # Handle response data here
        else:
            print("Request history: failed with status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("POST request failed:", e)

# !---------------------------------------------------------------< post record waste data >
def record_data():
    faculty = 'FIBO'
    machine_name = 'FIBO_1'
    waste_profile = 'plasticCan'
    weight = 5

    # auto generate: uuid, date, time after posted to url
    data = {
        'faculty': faculty,
        'machine_name': machine_name,
        'waste_profile': waste_profile,
        'weight': str(weight)
    }

    try:
        response = requests.post(url_post_data, json=data, verify=False)
        if response.status_code == 201:
            print("POST request successful (Created)")
            print("Response pose: "  + str(response.text))
            # Handle response data here
        elif response.status_code == 200:
            print("POST request successful (OK)")
            print("Response pose: "  + str(response.text))
            # Handle response data here
        else:
            print("POST request failed with status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("POST request failed:", e)

name = 'FIBO'
all_profile = get_all_machine_profile()

for entry in all_profile:
    create_date = entry['create_date']
    faculty = entry['faculty']
    machine_name = entry['machine_name']
    all_profiles = entry['all_profile']

    print(f"Create Date: {create_date}")
    print(f"Faculty: {faculty}")
    print(f"Machine Name: {machine_name}")
    print("All Profiles:")
    for profile in all_profiles:
        print(f" - {profile}")
    print()

    if name == faculty:
        print("T")

def print_cube(num):
    print("Cube: {}" .format(num * num * num))
 
 
def print_square(num):
    print("Square: {}" .format(num * num))
 
 
if __name__ =="__main__":
    t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_cube, args=(10,))
 
    t1.start()
    t2.start()
 
    t1.join()
    t2.join()
 
    print("Done!")