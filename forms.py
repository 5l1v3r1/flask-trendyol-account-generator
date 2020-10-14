from wtforms import Form,StringField,PasswordField,validators

class registerform(Form):
    username = StringField("Kullanıcı adı",validators=[validators.DataRequired("Bu alan dolu olmalıdır")])
    password = PasswordField("Şifre",validators=[validators.DataRequired("Bu alan dolu olmalıdır")])
    MailsPassword = StringField("Maillerin şifresi",validators=[validators.DataRequired("Bu alan dolu olmalıdır")])

class loginform(Form):
    username = StringField("Kullanıcı adı",validators=[validators.DataRequired("Bu alan dolu olmalıdır")])
    password = StringField("Şifre",validators=[validators.DataRequired("Bu alan dolu olmalıdır")])