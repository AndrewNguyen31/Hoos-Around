<p align="center">
    <img src="static/imgs/Logo.png" alt="logo" height="200" />
</p>

<h1 align="center">Hoo's Around</h1>

<p align="center">
A map-based exploration tool powered by QR code landmarks to encourage student exploration. 
</p>

<p align = "center">
    In order to get started, users will have to login on the top right with a Google account in order to access the website. Once logged in, click on the Google logo on the top right and hit refresh tasks. Once you have aquired you tasks, get hunting! If you feel that there is a location that must be on this site, feel free to submit a location request using the button.
</p>

## Setting Project Up

1. Clone the repo

```bash
git clone https://github.com/AndrewNguyen31/Hoos-Around
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Load some sample data into the database

```bash
python manage.py loaddata sample_data.json
```

4. Run the server

```bash
python manage.py runserver
```


## Project Phases

- [Requirements Elicitation](./docs/requirements_elicitation.pdf)
- [Scrum Master Report](./docs/scrum_master_report.pdf)

## Resources

- [GameUI Database](https://www.gameuidatabase.com/) has a lot of good resources considering the video-game based inspiration for the map design.
- [Snazzy Maps](https://snazzymaps.com/) are reskinned themes for Google Maps
- [UVA's brand guidelines](https://brand.virginia.edu) for official colors and fonts
- [Django QR Code Maker](https://pypi.org/project/django-qr-code/)
  - QR code creator based on [Sengo](https://pypi.org/project/segno/) which could be used if the QR code library starts acting up (a bit old)
- [Creating models with the dialog element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog)
  - Browsers have native support for modals and it is super easy. No need to use a library or JQuery or anything like that.

## Using the Project

### Sharing a Task with a Friend

https://github.com/uva-cs3240-f23/project-b-16/assets/27795014/5cbc8b38-974c-46a3-a15e-8df5461e54ae

Because exploring new places often happens with friends, Hoos Around gives you the option to send places to your friends through either the `navigator.share` or `navigator.clipboard` API.

### Posted QR Code

![IMG_3355](https://github.com/uva-cs3240-f23/project-b-16/assets/27795014/46532596-f50d-47e7-a4e9-ddcf7aa33373)

QR Codes which represent places are posted around grounds at the place to visit. These posters may even be hidden so that checking things off is more involved than scanning a QR code. For instance, the Student Health and Wellness may have you complete a scavenger hunt of all the recources at Student Health and Wellness.

### Checking off a Task

https://github.com/uva-cs3240-f23/project-b-16/assets/27795014/a16c7900-e239-491d-87d6-cb51ab439048

Clicking "check off task" on a webpage alone insufficient to explore all that grounds has to offer. For this reason, completing tasks with Hoos Around requires scanning a QR code posted on a poster at the location. The QR code is automatically generated and will check off any user who has that task.

## Design Samples

### QR Code Poster

<p align="center">
<img src="./docs/imgs/qrcodeposter.png" alt="qr code poster" />
</p>

> As a location provider, I want to be able to have people complete checking off their location by scanning a QR code.

### Share Sheet

<p align="center">
<img src="./docs/imgs/share_sheet.png" alt="exploration share sheet" />
</p>

> As a user, I want to share my exploration progress in a satisfying way to build intrinsic motivation.
