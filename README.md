# Duck Rating
Tool written in Python to calculate ratings from exported JSON tournament files.
#### Requirements

- [Python](https://www.python.org/downloads/source/)
- [Pyenv](https://github.com/pyenv/pyenv)
- [Poetry](https://python-poetry.org/docs/#installation)

#### Purpose

Create ratings from JSON files exported from KickerTool, Lets'Foos and Fast tournament programs.

#### How do I get set up?

1. Install requirements:
```bash
./install.sh
```

2. Directory Tree
```bash
    Duck Rating
    ├── files
    │   ├── csv             # Exported CSV ratings.
    │   ├── kicker          # Folder for KickerTool JSON files.
    │   ├── pretified       # Pretified JSON File folder.
    │   └── scraped         # Scraped elimination JSON part.
    ├── README.md
    ├── run.py              # Main script caller.
    └── scripts
        ├── get_csv.py      # Script for building CSV files from JSON.
        ├── other.py        # Additional scripts.
        ├── scraper.py      # Scraping elimination JSON script.
        └── standings.py    # Script for building tables and standings in terminal.
```

3. Run the following python script from project directory to generate CSV files and tables(If enabled).
```bash
./run.py
```

#### To Do
- ELO point system. Point value determined by winner/loser position.
- Separate ELO point and Local point system retaings.
- Postgres integrasion.
- OS/OD standings.
- Tournament tool detection (Lets'Foos and KickerTool).
- Stats tracking (Goals in/out, W/L Ratio, avarage tournament position, opponents etc.)
- WCS/International tournament integration.

#### Who do I talk to? ###

[Paulius Verseckas](mailto:verseckas.paulius@gmail.com)