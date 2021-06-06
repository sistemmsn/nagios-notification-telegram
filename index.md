## Scripts de notificación por telegram con grafica pnp4nagios


Nagios Core solo viene con una estructura básica para alertas de correo electrónico basadas en texto plano. Estos scripts están orientados para la mensajería en Telegram vienen con la  integración de PNP4Nagios,agrega visualización de problemas a las alertas y emojis.


Ejemplo de notificación de servicio:

### Imagen

![Ejemplo](/images/bottelegram.png)

- Nota: la contraseña de nagios `no` de debe de llevar caracteres extraños como: `$%"#.` ya que el plugin lo toma como otros valores y no como parte de la contraseña.

### Requerimiento

```markdown
Usa Python 2.7

pip install argparse
pip install json
pip install requests
pip install shutil
pip install time
pip install pathlib
```

### Agregare las partes ha modificar en el plugin esto aplica para ambos (HOST y SERVICES).

```markdown
#Historial de gráficos
graph_history  = 12
```

```markdown
# Url de tu pnp4nagios
pnp4nagios = "http://192.5.212.249/pnp4nagios/"
```

```markdown
#Download for img and user, passd

srvurl = requests.get(srvurl, auth=HTTPBasicAuth('usuario','contraseña'), stream=True)
``` 

- Creamos una carpeta en la siguiente ruta:

### /usr/local/nagios/

```markdown
mkdir img
```
- Otorgamos permisos a la carpeta y también al scritp:

```markdown
chown nagios:nagios /img*
chown nagios:nagios service_nagiostelegram.py
```

### Parametros en el command.cfg

```markdown
# Envio de notificaciones mediante Telegram.
define command {
  
    command_name     notify-host-by-telegram                
    command_line     $USER1$/host_nagiostelegram.py --token 0000000000:12345678998765432112345679987654312  --object_type host --contact "$CONTACTPAGER$" --notificationtype "$NOTIFICATIONTYPE$" --hoststate "$HOSTSTATE$" --hostname "$HOSTNAME$" --hostaddress "$HOSTADDRESS$" --output "$HOSTOUTPUT$"
}
define command {
  
    command_name     notify-service-by-telegram
    command_line     $USER1$/service_nagiostelegram.py --token 0000000000:12345678998765432112345679987654312 --object_type service --contact "$CONTACTPAGER$" --notificationtype "$NOTIFICATIONTYPE$" --servicestate "$SERVICESTATE$" --hostaddress "$HOSTADDRESS$" --hostname "$HOSTNAME$" --servicedesc "$SERVICEDESC$" --output "$SERVICEOUTPUT$"
}
```

### Parametros en el template.cfg


 ```markdown
define contact {

    name                            generic-contact         ; The name of this contact template
    service_notification_period     24x7                    ; service notifications can be sent anytime
    host_notification_period        24x7                    ; host notifications can be sent anytime
    service_notification_options    w,u,c,r,f,s             ; send notifications for all service states, flapping events, and scheduled downtime events
    host_notification_options       d,u,r,f,s               ; send notifications for all host states, flapping events, and scheduled downtime events
    service_notification_commands   notify-service-by-telegram  ; send service notifications via email
    host_notification_commands      notify-host-by-telegram ; send host notifications via email
    register                        0                       ; DON'T REGISTER THIS DEFINITION - ITS NOT A REAL CONTACT, JUST A TEMPLATE!
}
```

### Parametros en el contacs.cfg

-- Crearemos un nuevo contact name 

 ```markdown
define contact {
  contact_name                    Grupo_Chat_Telegram
  use				                      generic-contact
  pager				                    -110001000
  service_notification_commands   notify-service-by-telegram
  host_notification_commands      notify-host-by-telegram
}
```

- Nota una vez creado el contact name lo agregamos a nuesto contactgroup


<h2>Referencias</h2>

-- Agradezco al desarrollador inicial por crear el scritp, consulte [GitHub hvanderlaan](https://github.com/hvanderlaan).