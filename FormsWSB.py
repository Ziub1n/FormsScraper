from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
def start_bot():
    login = login_entry.get()
    password = password_entry.get()
    filepath = filepath_entry.get()

    if not filepath:
        messagebox.showerror("Błąd", "Podaj ścieżkę do pliku przed uruchomieniem bota.")
        return

    threading.Thread(target=run_selenium_bot, args=(login, password, filepath)).start()
def run_selenium_bot(login, password, filepath):
    options = Options()
    options.add_argument('--mute-audio')



    # Uruchomienie przeglądarki
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 40)

    # Logowanie
    driver.get(
        'https://lite-558550368093537651.myfreshworks.com/login?client_id=451980218021503405&redirect_uri=https%3A%2F%2Flite-assist.freshdesk.com%2Ffreshid%2Fauthorize_callback%3Fhd%3Dlite-assist.freshdesk.com')
    wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(login)
    wait.until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-o1ejds'))).click()

    time.sleep(40)
    b=0

    with open(filepath, 'r') as file:
        links = file.readlines()

    order_numbers_with_d = []
    order_numbers_without_d = []
    i = len(links)




    for link in links:
        link = link.strip()
        if not link:
            continue

        current_window_handle = driver.current_window_handle


        all_window_handles = driver.window_handles

        for window_handle in all_window_handles:

            if window_handle != current_window_handle:
                driver.switch_to.window(window_handle)
                driver.close()

        driver.switch_to.window(current_window_handle)

        driver.get(link)
        order_number_pattern = re.compile(r'D-[A-Z0-9]{14}|[A-Z0-9]{14}')
        time.sleep(1)
        spans = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//td[contains(@class, 'right-column')]/span[@class='ember-tooltip-target']")))

        dynamic_value = ""
        for span in spans:
            text_content = span.get_attribute('textContent').strip()
            if order_number_pattern.match(text_content):
                dynamic_value = text_content
                break
        time.sleep(1)



        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".user-name-link"))
        )
        element.click()


        window_handles = driver.window_handles


        driver.switch_to.window(window_handles[-1])


        time.sleep(1)

        script = """
        var range = document.createRange();
        range.selectNode(document.body);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        document.execCommand("copy");
        """

        driver.execute_script(script)


        copied_text = driver.execute_script("return window.getSelection().toString()")


        try:
            found_text = None
            for line in copied_text.split('\n'):
                candidate_text = line.strip()
                if len(candidate_text) == 28 and re.match("^[a-zA-Z0-9]+$", candidate_text):
                    found_text = candidate_text
                    break

            if found_text is None:
                found_text = "error"
                
        except Exception as e:
            found_text = "error"

        if dynamic_value:
            if dynamic_value.startswith("D-"):
                order_numbers_with_d.append((link.strip(), dynamic_value, found_text))
            else:
                order_numbers_without_d.append((link.strip(), dynamic_value, found_text))

        else:
            order_numbers_without_d.append((link.strip(), "XXXXXXXXXXXXXXXX", found_text))

        b += 1
        update_progress(b, i)
        time.sleep(1)



    # -------------------------------------------------------------ONFLEET---------------------------------------------------


    driver.get('https://onfleet.com/login?errorCode=1114')
    wait.until(EC.element_to_be_clickable((By.ID, 'email-button'))).click()

    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys('-')

    password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password_field.send_keys('-' + Keys.ENTER)

    # Zastąpione przez WebDriverWait, jeśli to konieczne
    # driver.execute_script("document.getElementById('submit-step').style.display = 'none';")

    # button = wait.until(EC.element_to_be_clickable((By.ID, 'submit-step')))
    # driver.execute_script("arguments[0].click();", button)
    time.sleep(40)
    input_order = wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="text" and @placeholder="Search"]')))

    def extract_part_after_phrase(text, phrase):
        if phrase in text:
            return text.split(phrase)[1].split()[0]
        return ""


    with open("Final_Jush.txt", "w") as file:

        for link, number, externalId in order_numbers_without_d:
            if number == "XXXXXXXXXXXXXXXX":
                file.write(link + '\n')
                file.write(externalId + '\n')
                file.write("no_rider_assigned\n\n\n")
                continue



            input_order.clear()
            time.sleep(1)
            input_order.send_keys(number + Keys.ENTER)

            try:
                time.sleep(2)
                div_element = driver.find_element(By.CLASS_NAME, 'listItem')
                div_element.click()
                time.sleep(1)
                assigned_worker_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="assignedWorkerName"]')))
                assigned_worker_name = assigned_worker_element.text

                details_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="detailsTaskDetails"]')))
                details_text = details_element.text

                order_number = extract_part_after_phrase(details_text, "Order number:")
                area_key = extract_part_after_phrase(details_text, "key:")

                print(link)
                print(externalId)
                print(area_key)
                print(order_number)
                print(assigned_worker_name)
                file.write(link + '\n')
                file.write(externalId + '\n')
                file.write(area_key + "\n")
                file.write(order_number + "\n")
                file.write(assigned_worker_name + "\n\n\n")
                time.sleep(1)

                done_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test-id="detailsTaskDoneBtn"]'))
                )
                done_button.click()

                time.sleep(2)
            except Exception:

                file.write(link + '\n')
                file.write(externalId + '\n')
                file.write("no_rider_assigned\n\n\n")

                done_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test-id="detailsTaskDoneBtn"]'))
                )
                done_button.click()



            time.sleep(1)


    driver.get('https://onfleet.com/login?errorCode=1114')
    wait.until(EC.element_to_be_clickable((By.ID, 'email-button'))).click()

    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys('-')

    password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password_field.send_keys('-' + Keys.ENTER)



    time.sleep(40)
    input_order = wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="text" and @placeholder="Search"]')))

    def extract_part_after_phrase(text, phrase):
        if phrase in text:
            return text.split(phrase)[1].split()[0]
        return ""


    with open("Final_Delio.txt", "w") as file:
        for link, number, externalId in order_numbers_with_d:
            if number == "XXXXXXXXXXXXXXXX":
                file.write(link + '\n')
                file.write(externalId + '\n')
                file.write("no_rider_assigned\n\n\n")
                continue

            input_order.clear()
            input_order.send_keys(number + Keys.ENTER)

            try:
                time.sleep(2)
                div_element = driver.find_element(By.CLASS_NAME, 'listItem')
                div_element.click()
                time.sleep(1)
                assigned_worker_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="assignedWorkerName"]')))
                assigned_worker_name = assigned_worker_element.text

                details_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="detailsTaskDetails"]')))
                details_text = details_element.text

                order_number = extract_part_after_phrase(details_text, "Order number:")
                area_key = extract_part_after_phrase(details_text, "key:")

                print(link)
                print(externalId)
                print(area_key)
                print(order_number)
                print(assigned_worker_name)

                file.write(link + '\n')
                file.write(externalId + '\n')
                file.write(area_key + "\n")
                file.write(order_number + "\n")
                file.write(assigned_worker_name + "\n\n\n")
                time.sleep(1)

                done_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test-id="detailsTaskDoneBtn"]'))
                )
                done_button.click()



            except Exception:

                file.write(link + '\n')
                file.write(externalId + '\n')
                file.write("no_rider_assigned\n\n\n")

                done_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test-id="detailsTaskDoneBtn"]'))
                )
                done_button.click()


            time.sleep(1)

    driver.close()
    driver.quit()


def choose_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    filepath_entry.delete(0, tk.END)
    filepath_entry.insert(0, filename)
    if filename:
        start_button.config(state="normal")
    else:
        start_button.config(state="disabled")

def save_file(filepath):
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if save_path:
        try:
            with open(filepath, 'r') as file:
                content = file.read()
            with open(save_path, 'w') as file:
                file.write(content)
            with open(filepath, 'w') as file:
                file.write('')
            messagebox.showinfo("Sukces", "Plik został zapisany i wyczyszczony.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił problem podczas zapisywania pliku: {e}")


def open_export_window():
    export_window = tk.Toplevel(root)
    export_window.title("Eksport wyników")
    export_window.geometry("300x100")

    export_delio_btn = tk.Button(export_window, text="Zapisz Final_Delio.txt", command=lambda: save_file("Final_Delio.txt"))
    export_delio_btn.pack(pady=5)

    export_jush_btn = tk.Button(export_window, text="Zapisz Final_Jush.txt", command=lambda: save_file("Final_Jush.txt"))
    export_jush_btn.pack(pady=5)



root = tk.Tk()
root.title("Automatyzacja Formularzy")
root.geometry("600x400")

progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=20)

login_label = tk.Label(root, text="Login:")
login_label.pack()
login_entry = tk.Entry(root)
login_entry.pack()

password_label = tk.Label(root, text="Hasło:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

filepath_label = tk.Label(root, text="Ścieżka do pliku:")
filepath_label.pack()
filepath_entry = tk.Entry(root)
filepath_entry.pack()
choose_file_btn = tk.Button(root, text="Wybierz plik", command=choose_file)
choose_file_btn.pack()

start_button = tk.Button(root, text="Start", command=start_bot, bg='red', fg='green', state="disabled")
start_button.pack()

export_results_btn = tk.Button(root, text="Otwórz wynikowe pliki", command=open_export_window)
export_results_btn.pack()

def update_progress(i, total):

    progress_percent = (i / total) * 100

    if progress_percent >= 100:
        progress_percent = 0


    progress['value'] = progress_percent


    percent_label.config(text=f"{progress_percent:.2f}%")



progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=20)


percent_label = tk.Label(root, text="0%")
percent_label.pack()


root.mainloop()