from flask import Flask, render_template, request 

app = Flask(__name__)

def water_usage_calculate(num_people, num_faucets, shower_time):
    # Basit bir su tüketimi hesaplama modeli
    base_people_usage = num_people * 50  # Kişi başına ortalama 50 litre
    faucet_usage = num_faucets * 10      # Her çeşme başına 10 litre
    shower_usage = shower_time * 12      # Duş başına dakika başına 12 litre

    daily_usage = base_people_usage + faucet_usage + shower_usage
    weekly_usage = daily_usage * 7
    monthly_usage = daily_usage * 30

    return daily_usage, weekly_usage, monthly_usage
@app.route('/dus', methods=['GET'])
def show_form():
    return render_template('form.html')

@app.route('/calculate_shower_duration', methods=['POST'])
def calculate_shower_duration():
    shower_option = request.form['shower_option']
    result = calculate_shower_duration(shower_option)
    return render_template('son.html', result=result)



# Duş süresini hesapla
def calculate_shower_duration(shower_option):
    if shower_option == "5":
        return 5
    elif shower_option == "15-25":
        return 20
    elif shower_option == "30+":
        return 35
    else:
        return 10  # Varsayılan olarak 10 dakika

@app.route('/people_count/<int:count>')
def people_count(count):
    # Display the number of people and collect further information
    return render_template('cesme.html', count=count)

@app.route('/faucet_selection/<size>/<int:faucets>')
def faucet_selection(size, faucets):
    # Display selected faucet size and number, and collect additional info if needed
    return render_template('dus.html', size=size, faucets=faucets)


@app.route('/shower_duration/<size>', methods=['GET'])
def shower_duration(size):
    # Kullanıcının seçtiği duş süresini alın
    shower_option = request.args.get('duration')

    # result değişkenini hesapla
    result = calculate_shower_duration(shower_option)
    
    # son.html şablonuna result değişkenini ileterek render_template ile döndür
    return render_template('son.html', size=size, faucets=1, result=result)

# İlk sayfa, kullanıcıdan evde yaşayan kişi sayısını alır
@app.route('/')
def index():
    return render_template('index.html')

# İkinci sayfa, çeşme sayısını toplar
@app.route('/cesme', methods=['POST'])
def faucets():
    num_people = int(request.form['num_people'])
    return render_template('cesme.html', num_people=num_people)

# Üçüncü sayfa, duş süresini alır
@app.route('/dus', methods=['POST'])
def shower():
    num_people = int(request.form['num_people'])
    num_faucets = int(request.form['num_faucets'])
    return render_template('dus.html', num_people=num_people, num_faucets=num_faucets)

# Sonuç sayfası, tüm girişler toplandıktan sonra su tüketimini hesaplar ve sonucu gösterir
@app.route('/result', methods=['POST'])
def result():
    num_people = int(request.form['num_people'])
    num_faucets = int(request.form['num_faucets'])
    shower_time = int(request.form['shower_time'])
    daily_usage, weekly_usage, monthly_usage = water_usage_calculate(num_people, num_faucets, shower_time)
    return render_template('son.html', daily_usage=daily_usage, weekly_usage=weekly_usage, monthly_usage=monthly_usage)

# Form
@app.route('/form')
def form():
    return render_template('form.html')

#Formun sonuçları
@app.route('/submit', methods=['POST'])
def submit_form():
    # Veri toplama için değişkenleri tanımlayın
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    date = request.form['date']
    phone_number = request.form['phone_number']
    gender = request.form['gender']
    selected_options = request.form.getlist('selected_options')
    city = request.form['city']
    region = request.form['region']
    with open('form.txt', 'a',) as f:
        f.write(name + email + address + date + '\submit')

    # Verilerinizi kaydedebilir veya e-posta ile gönderebilirsiniz
    return render_template('form_result.html', 
                           # Değişkenleri buraya yerleştirin
                           name=name,
                           email=email,
                           date=date,
                           address=address,
                           phone_number=phone_number,
                           gender=gender,
                           city=city,
                           selected_options=selected_options,
                           region=region,
                           )
    


if __name__ == "__main__":
    app.run(debug=True)
