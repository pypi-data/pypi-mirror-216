# ConsumableAI

## Overview

Consumable AI is an SDK that can be easily integrated into the self hosted BI tools which gives enterprises the power to talk to the databases in natural language. This will make exploratory data analyses easy to perform and remove the barrier of acquiring SQL skills and database know-how.

## Installation

A Python library for seamless integration with ConsumableAI platform.

> Right now we only support postgresql database, soon will update other databases as well

To get started, follow these steps:

1. Set up a virtual environment in your aws which has access to database:

   $ python3 -m venv myenv
   $ source myenv/bin/activate

2. Install the ConsumableAI library using pip:

   $ pip install consumableai

3. Obtain an API key by visiting [https://platform.consumableai.com](https://platform.consumableai.com) and creating an account. The API key will be used to authenticate your requests.

4. Initialize the ConsumableAI library:

   $ consumableai init

   This command will prompt you to enter various database-related values. The library will create the table schema for your data. Please note that ConsumableAI does not store your data directly. Instead, it creates the table schema and shares a link to a spreadsheet. You can make changes to the spreadsheet, and when you're ready, inform us to update the schema accordingly.

   The spreadsheet link will be provided after initialization.

For more information and documentation, please visit our website at [https://platform.consumableai.com](https://platform.consumableai.com).

Happy data exploration with ConsumableAI!
