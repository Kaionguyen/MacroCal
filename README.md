## WIP
Theres still several features to be implemented:
* Edamam api endpoints
  * food lookup
  * nutrition analysis
  * recipe search
* Diet Tracker

## Current Features
* Get estimated daily calorie intake and different macro distributions fit to your needs using the [macrocalculator amounts](https://rapidapi.com/malaaddincelik/api/fitness-calculator/)
  * Available for ***registered*** and ***unregistered users***
https://github.com/Kaionguyen/MacroCal/assets/107159508/7b9a8727-db6f-48cb-8e4b-9e33b6a89467
<br>https://github.com/Kaionguyen/MacroCal/assets/107159508/4024eac3-ca73-41ae-bd5f-3b6064f2bd56
* Download a preformatted xlsx spreadsheet to track meals outside of web app
  * ***Only*** available to ***registered*** users
* Registered users will have their information saved into database

## Spreadsheets
Comprised of 5 sheets (Stats, Balanced, Low Fat, Low Carbs, High Protein). 
### Stats Sheet
Only serves to track progression over time and is unfortunately ***NOT DYNAMIC***. Creating a dynamic sheet would have
required Excel VBA *(Visual Basic for Applications)* and a .xlsm file download which pose a potential ***security risk*** for the user downloading the file. 
So I just chose not to use it for the sake of less code and user peace of mind 🙏.

<br>![image](https://github.com/Kaionguyen/MacroCal/assets/107159508/53f14d38-3bd2-4eb4-8b07-a1ba89783d8d)

Very Simple!🙀

### Macro Sheets
The remaining 4 sheets are all formatted the same, but will have a slightly different macros appended to the "Goals" table. Simply input
the date of the meal, the type, name, and it's calories and macros. The "Remaining" table will automatically calculate how much is needed from the most recent entries *(by date not position)*.

<br><img width="1608" alt="image" src="https://github.com/Kaionguyen/MacroCal/assets/107159508/14b7485b-01eb-40d2-aa68-d7feb9b64bf9">
As you can see, it's calculating the remainder for 9/5/23 which only has 5 of each macro.
