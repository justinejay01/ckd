from flask import Flask, render_template, request
from food_recommendation_model import FoodRecommendationModel
import joblib
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='Templates')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Dietary'

mysql = MySQL(app)
model = joblib.load('model.sav')
model2 = joblib.load('food_recommendation_model.sav')

@app.route('/predict', methods=['POST'])
def predict():
    name = request.form['name']
    creatinineUMOL = float(request.form['serumCr'])
    age = float(request.form['age'])
    sex = request.form['gender']
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    serum_potassium = float(request.form['serum_Potassium'])
    
    creatinine = creatinineUMOL * 0.011312217194570135

    # calculate eGFR based on gender and SCr value in mg/dL
    if sex == "Female":
        if creatinine < 0.7:
            eGFR = 144 * (creatinine / 0.7) ** -0.329 * (0.993 ** age)
        else:
            eGFR = 144 * (creatinine / 0.7) ** -1.209 * (0.993 ** age)
    else:
        if creatinine < 0.9:
            eGFR = 141 * (creatinine / 0.9) ** -0.411 * (0.993 ** age)
        else:
            eGFR = 141 * (creatinine / 0.9) ** -1.209 * (0.993 ** age)

    # Make prediction using the loaded model
    male = 1 if sex == 'Male' else 0
    prediction = model.predict(
        [[creatinine, age, male, eGFR, height, weight]])[0]

    recommendation = model2.get_recommendations(serum_potassium)
    recommendation_serialized = ', '.join(map(str, recommendation))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name FROM checkup WHERE name = %s", [name])
    result = cursor.fetchone()
    if result is not None:
        cursor.execute("UPDATE checkup SET age = %s, Gender = %s, Weight = %s, Height = %s, eGFR = %s, CKD_STATUS = %s, Potassium = %s, Creatinine = %s, recommended_foods = %s WHERE name = %s", [
                       age, sex, f'{weight} kg', f'{height} cm', f'{round(eGFR, 2)} mL/min/1.73m²', f'Stage {prediction}', f'{serum_potassium} mmol/L', f'{creatinineUMOL} µmol/L', recommendation_serialized, name])
    else:
        cursor.execute("INSERT INTO checkup (name,age,Gender,Weight,Height,eGFR,CKD_STATUS,Potassium,Creatinine,recommended_foods) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [
            name, age, sex, f'{weight} kg', f'{height} cm', f'{round(eGFR, 2)} mL/min/1.73m²', f'{get_ckd_status_string(prediction)}', f'{serum_potassium} mmol/L', f'{creatinineUMOL} µmol/L', recommendation_serialized])
    mysql.connection.commit()
    cursor.close()
    return render_template('process_checkup.html', name=name.title(), prediction=prediction, recommendation=recommendation, error=False)

def get_ckd_status_string(stage):
    if stage == 2:
        return "Stage 2 Mild"
    elif stage == 3:
        return "Stage 3 Moderate"
    elif stage == 4:
        return "Stage 4 Severe"
    elif stage == 5:
        return "Stage 5 Kidney Failure"
    else:
        return "Unknown Stage"

if __name__ == '__main__':
    app.run(port=8000)
