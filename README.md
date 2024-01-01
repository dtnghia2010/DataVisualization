# INTERACTIVE CHART PROJECT
Course: Algorithms & Data Structures


![interactive_chart](https://github.com/dtnghia2010/DataVisualization/assets/126145844/be4e860c-6177-4c44-84c5-39b69851b98b)



<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/dtnghia2010/DataVisualization">
  </a>

<h3 align="center">Interactive Chart Project</h3>
<h4 align="center">Team Name: Hội người liều!</h4>

  <p align="center">
    A website dashboard created with Python and HTML for Data Structure Argorithm course in International University - VNUHCM!
    <br />
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
# Table of contents :round_pushpin:
1. [Introduction](#Introduction)
2. [Tech stack](#Tech_stack)
3. [Charts](#Charts)
4. [Features](#Features)
5. [Challenges](#Challenges)
6. [Acknowledgments](#Acknowledgments)
7. [References](#References)

<!-- ABOUT THE PROJECT -->

## 1. Introduction <a name="Introduction"></a> :bricks:

<div align="center">
<img src="screenshots/Intro.gif" alt="">
</div>

<div style="text-align:justify">
Welcome to our first data visualization website! This is a platform designed to present information, data, and insights in visually appealing and comprehensible ways. It leverages various graphical elements such as charts, graphs, maps, infographics, and dashboards to help users interpret complex data easily.
</div>

### Team Members :couplekiss_man_man:

| Order |         Name          |     ID      |                  Email                  |                       Github account                        |                      
| :---: | :-------------------: | :---------: |:---------------------------------------:| :---------------------------------------------------------: | 
|   1   |     Dương Trọng Nghĩa      | ITITIU21256 |           ITITIU21256@student.hcmiu.edu.vn           |           [dtnghia2010](https://github.com/dtnghia2010)         |
|   2   | Ngô Thị Thương | ITCSIU21160 |          ITCSIU21160@student.hcmiu.edu.vn           | [thuongngo050902](https://github.com/thuongngo050902) |           |
|   3   | Nguyễn Phạm Kỳ Phương | ITITIU21287 |        ITITIU21287@student.hcmiu.edu.vn         |       [npkyphuong04](https://github.com/npkyphuong04)       |      |
|   4   | Nguyễn Anh Thắng| ITCSIU21233 |                     ITCSIU21233@student.hcmiu.edu.vn                   |       [nathang0147](https://github.com/nathang0147)      |


### Installation :dart:

1. Open the terminal on your IDE
2. Clone the repo
   ```sh
   git clone https://github.com/dtnghia2010/DataVisualization
   ```
3. Check the file status
   ```sh
   git status
   ```
4. Change branch
   ```js
   git checkout 'branch_name'
   ```
5. Install Django Framework
   - Windows:
     ```sh
     py -m pip install Django
     ```
   - Unix/MacOS:
     ```sh
     python -m pip install Django
     ```
7. Download some pakages of the project
   ```sh
   pip install pandas
   ```
   ```sh
   pip install matplotlib
   ```
   ```sh
   pip install sikit-learn
   ```
   ```sh
   pip install django-import-export
   ```
   ```sh
   pip install numpy
   ```


</div>

### Task Allocation :

| Order | Task                                  |  Person   | Contribution (%) |
| :----: |:--------------------------------------:| :-------: | :----------: |
| 1     | Search Algorithm, Visualize Add_data and Upload_file |  Ngô Thương  |     25      |
| 2     |Linear Regression, Upload_file with CSV   | Trọng Nghĩa |      25      |
| 3     | Interface, Delete Data          | Kỳ Phương |      25      |
| 4     | Sort Algorithm, Rename Chart     | Anh Thắng  |      25      |



<br />


## 2. Tech stack <a name="Tech_stack"></a>:joystick:
### :art:Front-end:
  - Language: [Python](https://www.python.org/)
  - Framework: [Django](https://www.djangoproject.com/)
  - Web Dev: [HTML](https://www.w3schools.com/html/), [CSS](https://www.w3schools.com/css/), [Bootstrap](https://getbootstrap.com/)
  - Compiler: [PyCharm](https://www.jetbrains.com/pycharm/download/?section=windows)

    
### :hammer_and_wrench:Back-end:
  - Language: [Python](https://www.python.org/)
  - Framework: [Django](https://www.djangoproject.com/)
  - Compiler: [PyCharm](https://www.jetbrains.com/pycharm/download/?section=windows)
<br />


## 3. Charts <a name="Charts"></a>:bar_chart:
- In this project, we use templates from [Chart.js](https://www.chartjs.org/) to generate charts.
- Example code to create a chart
  ```ruby
  <!-- Display your chart here using listlabels and listdatas -->
  <canvas id="myChart" width="400" height="400" class="mb-4 pt-3"></canvas>
  <script>
            var ctx = document.getElementById('myChart').getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: {{ listlabels|safe }},
                    datasets: [{
                        label: 'Attribute2',
                        data: {{ listdatas|safe }},
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
  </script>
  ```
<br />


## 4. Features <a name="Features"></a>:robot:
We have 2 main parts divided specifically: Add Data & Upload File. In each part, we use some features like algorithms to express them. Furthermore, we have developed one more extra feature, which is Linear Regression Algorithms - Prediction Data.

![add_upload](https://github.com/dtnghia2010/DataVisualization/assets/126145844/0f5298df-fbfd-4cd1-89b2-ce19ac653bc9)

<br />

### :heavy_check_mark:Add Data:

In this field, we use some features, such as:
- Sorting Algorithm (Quick Sort Algorithm)
- Searching Algorithm (Binary Search Algorithm)
- Delete Data

![add_data](https://github.com/dtnghia2010/DataVisualization/assets/126145844/aa148ada-f1bc-40b2-bbab-88f499348f97)

<br />

### :heavy_check_mark:Upload File:

We need to provide a file that has the '.csv' extension. Therefore, the algorithms below will be used appropriately:
- Sorting Algorithm (Quick Sort Algorithm)
- Searching Algorithm (Binary Search Algorithm)

![upload_file](https://github.com/dtnghia2010/DataVisualization/assets/126145844/68701b3c-c8ef-4f31-9d2a-046334640392)

<br />

### :heavy_check_mark:Extra Feature: Linear Regression Algorithms:

Linear Regression is a supervised learning algorithm which is both a Statistical and a Machine Learning Algorithm. Based on the supplied input value X, it is used to foresee the real-valued output Y. 
</br>
Similar to the Upload File section, we also need to input a file with the extension '.csv', so that the data can be converted to chart form using 'matplotlib'.
- First, we provide a file 'testData.csv' - containing population data of countries around the world; next, enter the values ​​'Brazil', '2014', '2022', '2023' into the blanks such as Label, From, To, Prediction, respectively:
  
  ![input_predict](https://github.com/dtnghia2010/DataVisualization/assets/126145844/d9344a31-eb9d-410e-bbcc-76c59b894e61)



- Then, we will have a result like this:

  ![predict](https://github.com/dtnghia2010/DataVisualization/assets/126145844/e23605f3-c93f-44fa-bf36-dbe8d529d422)

<br />


<!-- CHALLENGES -->
## 5. Challenges <a name="Challenges"></a>
- Task allocation for each team member
- Using platform for communication
<br />


## 6. Acknowledgments<a name="Acknowledgments">:brain:
<div style="text-align:justify">
We would want to express our gratitude to Dr. Vi Chi Thanh for providing us with the chance to
participate in this project and apply what we learned in theory into practice. 
</div>
<br />


## 7. References<a name="References">:bookmark:
- [Python tutorial](https://www.w3schools.com/python/)
- [Django tutorial](https://youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&si=RdGOno3cRHiOUGgr)
- [Add Data & Chart](https://www.youtube.com/watch?v=a1j8g01ics4&t=1817s)
- [Read '.csv' file](https://www.youtube.com/watch?v=Y7OAk7DiLJs&t=1474s)
- [Django and matplotlib integration](https://www.youtube.com/watch?v=jrT6NiM46jk&list=PL_yx8AXzzvNxJ0bA4-WKsJ7cpQm8w0Ef5&index=23)
- [Linear Regression Implementation From Scratch using Python](https://www.geeksforgeeks.org/linear-regression-implementation-from-scratch-using-python/)

<br />

<p align="right">(<a href="#top">Back to top</a>)</p>
</div>


[contributors-shield]: https://img.shields.io/github/contributors/dtnghia2010/DataVisualization.svg?style=for-the-badge
[contributors-url]: https://github.com/dtnghia2010/DataVisualization/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/dtnghia2010/DataVisualization.svg?style=for-the-badge
[forks-url]: https://github.com/dtnghia2010/DataVisualization/network/members
[stars-shield]: https://img.shields.io/github/stars/dtnghia2010/DataVisualization.svg?style=for-the-badge
[stars-url]: https://github.com/dtnghia2010/DataVisualization/stargazers
[issues-shield]: https://img.shields.io/github/issues/dtnghia2010/DataVisualization.svg?style=for-the-badge
[issues-url]: https://github.com/dtnghia2010/DataVisualization/issues
