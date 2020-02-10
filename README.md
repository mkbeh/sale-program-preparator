# sale-program-preparator

Simple cli utility for preparing cloned program for 
sale or something else.

**Features**
* Removes directories and files
    * .idea
    * .vscode
    * .git
    * .gitignore
* Checks license in require files
    
    Exclude:
    * LICENSE
    * README.md
* Archives program


## Usage

### Options

* **remote-repository** - receives URL of remote repository
such as github/gitlab
* **check-license** - checks the license text in each
file , exclude: LICENSE and README.md
* **archive** - archives prepared directory of cloned
repository.