Tento projekt jsem vytvořil k ukázce svých schopností v programovacím jazyce Python.
Jedná se o zpracování známé hry „Chcete být milionářem?“ v počítačové verzi za použití enginu pygame.
Jakožto výchozí otázky jsem použil otázky z fotbalového prostředí. Některé jsou přejaté z https://www.kopacak.cz/hry/fotbalovymilionar, některé jsou vlastním dílem.

Hráč obdrží postupně patnáct otázek. Ke každé otázce dostane čtyři odpovědi, přičemž právě jedna z nich je správná.
Pokud hráč odpoví správně, postupuje na další otázku. Pokud hráč odpoví chybně, hra končí.
Hráč může také využít tří nápovědy: 50/50 (odstraní dvě špatné odpovědi), pomoc od přítele a pomoc od publika. Poslední dvě nápovědy mají větší chybovost tím, jak daleko hráč ve hře postupuje.
Pokud hráč odpoví správně na všechny otázky, vyhrává milion. V originále dolarů, v mém zpracování pouze herních bodů.
Pokud hráč odpoví špatně, hra končí a jeho skóre se vrátí na poslední záchytný bod. Záchytné body jsou na otázkách 0, 5 a 10.
Hráč může také kdykoliv hru ukončit, čímž si odnese skóre, které v tuto chvíli má (bez návratu na záchytný bod).

Po konci hry může hráč uložit své nahrané skóre. V tabulce highscores.csv se ukládá 10 nejlepších výkonů.
Kromě hraní hry může uživatel v programu také přidat novou otázku nebo zobrazit nejlepší výsledky. Ty se také zobrazí po uložení skóre.

Program používá externí knihovny:
pygame – engine, na kterém hra běží
matplotlib.pyplot – k zobrazení sloupcového grafu „odpovědí publika“

Dále používá moduly:
csv – ze souborů csv se načítají otázky, různé texty (labels) i s pozicemi a velikostí textu a také nejlepší výkony
datetime – uložená skóre také zaznamenávají současný datum a čas
operator – pro řazení skóre v tabulce
os – k operaci se soubory
random – k randomizaci pořadí odpovědí, nahraných otázek nebo výsledků nápověd

Celý projekt je napsaný v angličtině, včetně UI, otázky jsou však napsány v češtině.




I created this project to demonstrate my skills in the Python programming language.
It is a rework of the well-known game "Who wants to be a millionaire?" in a computer version using the pygame engine.
I used questions from a football environment as the default questions. Some are taken from https://www.kopacak.cz/hry/fotbalovymilionar, some are my own work.

The player receives fifteen questions in sequence. For each question he gets four answers, with exactly one of them being correct.
If the player answers correctly, they move on to the next question. If the player answers incorrectly, the game ends.
The player can also use three hints: 50/50 (removes two wrong answers), help from a friend, and help from the audience. The last two hints have a higher error rate the further the player progresses in the game.
If the player answers all the questions correctly, he wins a million. In the original dollars, in my version only game points.
If a player answers wrong, the game ends and his score reverts to the last checkpoint. The checkpoints are on questions 0, 5 and 10.
The player can also end the game at any time, taking the score he has at that moment (without returning to the checkpoint).

At the end of the game, the player can save his accumulated score. The highscores.csv table stores the top 10 performances.
In addition to playing the game, the user can also add a new question or view the best scores in the program. Best scores will also be displayed after saving the scores.

The program uses external libraries:
pygame - the engine on which the game runs
matplotlib.pyplot - to display a bar chart of "audience responses"

It also uses modules:
csv - CSV files are used to to load questions, different texts (labels) with positions and text size, and also best performances
datetime - the saved scores also record the current date and time
operator - for sorting scores in a table
os - to operate with files
random - to randomise the order of answers, loaded questions or results of hints

The whole project is written in English, including the UI, but the default questions are written in Czech.