# Detecting Insider Attacks on Databases using Blockchain
Here is a Demo of its working :smiley: (*For better resolution, [watch this](https://raw.githubusercontent.com/Miraj50/Blockchain-Database/master/assets/BcD_Demo.gif) in Full Screen mode*).

![Insider Attack Demo](assets/BcD_Demo.gif)
Note that during the Demo, *Multichain* was already running on the system (single node).

## Schema of the Database

* #### Credentials Table
    
    |Field|Type|Null|Key|
    |:---:|:---:|:---:|:---:|
    |uid|varchar(128)|NO|PRI|
    |salt|varchar(64)|YES||
    |hash|varchar(64)|YES||

* #### Grades Table

    |Field|Type|Null|Key|
    |:---:|:---:|:---:|:---:|
    |uid|varchar(128)|NO|PRI|
    |course|varchar(10)|NO|PRI|
    |grade|varchar(2)|YES||
    |txid|varchar(64)|YES||
    |identifier|varchar(128)|YES||

## Commands for Multichain:
1. **Start Node**
    * `$ multichain-util create chain1`
    * `$ multichaind chain1 -daemon`
    
2. **Create Streams**
    * `$ create stream stream1 false`
    * `$ subscribe stream1`
    * `$ create stream pubkey false`
    * `$ subscribe pubkey`
    * `$ create stream instructor false`
    * `$ subscribe instructor`
    
3. **Publish the courses of instructors** (*Course is hex encoded*)
    * `$ publish instructor ss 6373333137` <sub><sup>(InstructorID = <b>ss</b> and course = <b>cs317</b>)</sup></sub>
    * `$ publish instructor ss 6373333837` <sub><sup>(InstructorID = <b>ss</b> and course = <b>cs387</b>)</sup></sub>
    * `$ publish instructor puru 6373333333` <sub><sup>(InstructorID = <b>puru</b> and course = <b>cs333</b>)</sup></sub>
<hr>

 ### A full Report of the ***Protocol*** and the ***Implementation*** can be [found here](BlockchainDB_Report.pdf).
<hr>

#### COPYRIGHT and LICENSE

All the source files are licensed under GNU GLPv3 license. Refer [LICENSE](https://github.com/Miraj50/Blockchain-Database/blob/master/LICENSE) for more details.

    This project demonstrates detection of insider attacks on databases using Blockchain.

    Copyright (C) 2018  Rishabh Raj
    This code is licensed under GNU GPLv3 license. See LICENSE for details

    This project is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
