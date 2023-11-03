<a name="readme-top"></a>

# [Si Depi Application (Deteksi Pintar)](https://github.com/ptirtekdevelop/Si_Depi.git)

Smart detection app to detect road damage and calculate the amount of damage to road bending pavement.
<br />
[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#create-database">Create Database</a></li>
        <li><a href="#running-program">Running Program</a></li>
      </ul>
    </li>
    <li><a href="#feature">Features</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## About The Project
[![Product Name Screen Shot][product-screenshot]](https://example.com)

## Getting Started
### Prerequisites
For maximum results, please follow the following requirements:
- Use python >= 3.10
- Minimum RAM >= 4GB 
- OS Linux: (Ex: Ubuntu 22.04)

### Installation
Based application is python program you need to use the application and install based the instruction below.
1. Install python
```
sudo apt install python3.10
```
2. Clone the repo
```
git clone https://github.com/ptirtekdevelop/Si_Depi.git
```
3. Install library on OS
```
sudo apt-get update && sudo apt-get upgrade

```
```
sudo apt-get install libmysqlclient-dev default-libmysqlclient-dev build-essential pkg-config mysql-server python3-virtualenv
```
4. Create virtual environment
- Open terminal and enter to github directory has been clone or download
```
cd Si_Depi
```
- Create environment
```
virtualenv env
```
- Activate enviroment
```
source env/bin/activate
```
5. Install library for application
```
pip3 install --upgrade pip
pip3 install -r requirements.txt
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Create Database
1. Open terminal, run the command for enter database and enter
```
sudo mysql
```
2. Create database
```
CREATE DATABASE IRTEK_ROAD;
```
3. Create user
```
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```
4. Out from database
```
EXIT;

```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Running Program
Make sure you are in Si Depi Directory
1. Set environment application
```
export FLASK_APP=run.py
export FLASK_ENV=production
```
2. Running Program
```
python3 run.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Features
- `Framework`: Flask
- `Database`:  `SQLite`, MySql
- `DB Tools`: SQLAlchemy ORM
- `WebSockets`: Socketio
- `Authentication`, Session Based
- `Base template`: Volt Boostrap 5, Bootstrap, CSS

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

IRTEK - pt.irt2022@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/ptirtekdevelop/Si_Depi
[contributors-url]: https://github.com/ptirtekdevelop/Si_Depi/graphs/contributors

[license-shield]: https://img.shields.io/github/license/ptirtekdevelop/Si_Depi
[license-url]: https://github.com/ptirtekdevelop/Si_Depi/blob/main/LICENSE

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/company/pt-inovasi-rekayasa-teknologi-irtek/

[product-screenshot]: apps/static/assets/img/screenshot/output.jpg
