from PIL import ImageTk
from selenium.webdriver import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from tkinter import PhotoImage
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from tkinter import Tk, Label, Button, Listbox, PhotoImage
from PIL import Image, ImageTk

matrix = []
driver = None
def wczytaj_plik():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        with open(filename, 'r', encoding='utf-8') as file:
            tekst = file.read()
        global matrix
        matrix = [list(filter(None, rekord.split('\n'))) for rekord in tekst.strip().split('\n\n')]
        przycisk_gotowe['state'] = 'normal'



def automatyzacja_formularza(rekord):
    global driver
    if not driver:
        options = Options()
        options.add_argument('--mute-audio')
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    driver.get('https://lite-tech.typeform.com/to/viRo8oak')
    time.sleep(1)

    current_window_handle = driver.current_window_handle


    all_window_handles = driver.window_handles


    for window_handle in all_window_handles:

        if window_handle != current_window_handle:
            driver.switch_to.window(window_handle)
            driver.close()


    driver.switch_to.window(current_window_handle)

    wait = WebDriverWait(driver, 10000)

    # Wpisanie emaila
    input_mail = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.InputField-sc-__sc-26uh88-0.dEBNmz')))
    login = login_entry.get()
    input_mail.send_keys(login)

    time.sleep(1)
    element_do_klikniecia = driver.find_element(By.CSS_SELECTOR, 'div.TextWrapper-sc-__sc-1f8vz90-0.gbnXlt mark')
    ActionChains(driver).move_to_element(element_do_klikniecia).click().perform()

    time.sleep(1)

    input_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.InputField-sc-__sc-26uh88-0.iEpWNi')))
    input_element.send_keys(rekord[0])
    input_element.send_keys(Keys.ENTER)

    input_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.InputField-sc-__sc-26uh88-0.iEpWNi')))
    input_element.send_keys(rekord[1])
    input_element.send_keys(Keys.ENTER)

    input_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.InputField-sc-__sc-26uh88-0.dEBNmz')))
    input_element.send_keys(rekord[2])
    input_element.send_keys(Keys.ARROW_DOWN)
    input_element.send_keys(Keys.ENTER)

    time.sleep(1)

    input_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.InputField-sc-__sc-26uh88-0.iEpWNi')))
    input_element.send_keys(rekord[3])
    input_element.send_keys(Keys.ENTER)

    input_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.InputField-sc-__sc-26uh88-0.iEpWNi')))
    input_element.send_keys(rekord[4])
    input_element.send_keys(Keys.ENTER)

    time.sleep(1)


def kopiuj_do_schowka(event):
    wybrany_index = listbox.curselection()
    if wybrany_index:
        wybrany_link = listbox.get(wybrany_index)
        root.clipboard_clear()
        root.clipboard_append(wybrany_link.split(" ", 1)[1])

def uruchom_selenium():
    global driver
    if matrix:

        rekord = matrix.pop(0)
        listbox.insert(tk.END, f"{len(matrix) + 1}. {rekord[0]}")
        threading.Thread(target=automatyzacja_formularza, args=(rekord,)).start()
    else:

        messagebox.showinfo("Informacja", "Brak więcej formularzy.")


root = tk.Tk()
root.title("Automatyzacja Formularzy")
root.geometry("600x400")

login_label = tk.Label(root, text="Login:")
login_label.pack()
login_entry = tk.Entry(root)
login_entry.pack()


wczytaj_button = tk.Button(root, text="Wczytaj plik", command=wczytaj_plik)
wczytaj_button.pack()

przycisk_gotowe = tk.Button(root, text="Gotowe", state='disabled', command=uruchom_selenium)
przycisk_gotowe.pack()

listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH, expand=True)
listbox.bind('<Double-1>', kopiuj_do_schowka)

root.mainloop()


root.mainloop()
