# thanosql-magic

## Introduction

`thanosql-magic` is a Jupyter Notebook extension that provides SQL query capabilities using [ThanoSQL](https://www.thanosql.ai). This magic extension enables users to interact with ThanoSQL Workspace databases using extended SQL syntax within a Jupyter notebook.

`thanosql-magic` uses IPython magic. [IPython magic](https://ipython.readthedocs.io/en/stable/interactive/magics.html) is a special command that can be used in the IPython shell to perform specific tasks before executing the code. Since Jupyter includes the IPython shell, you can also use these magic commands in Jupyter Notebook.

IPython magic commands are prefixed with % or %% and % applies the magic to a single line of code, while %% applies the magic to multiple lines of code.

## Installation

To install thanosql-magic, you can use pip:

```
pip install thanosql-magic
```

Once installed, you can load the extension in your Jupyter notebook by running:

```python
%load_ext thanosql
```

## Usage

After loading the extension, you can connect to your ThanoSQL Engine instance by setting the thanosql variable:

1. Setting API_TOKEN

   ```python
   %thanosql API_TOKEN=<Issued_API_TOKEN>
   ```

1. Changing the Default API URI (Optional)

   ```python
   %thanosql http://localhost:8000/api/v1/query
   ```

3. Using Magic Commands

   You can then execute SQL queries on your Thanos data using the %thanosql magic command:

   ```python
   %%thanosql
   SELECT * FROM users
   ```

   This will run the SQL query and display the results in your Jupyter notebook.

You can also refer to the guide provided in [ThanoSQL's official documentation](https://docs.thanosql.ai/getting_started/hello_ThanoSQL/#3-check-the-list-of-the-thanosql-models-and-datasets-using-the-list-query-syntax).

## Requirements
- Python 3.x
- Jupyter Notebook

## Contributing
If you find any issues or would like to contribute to thanosql-magic, feel free to submit a pull request or open an issue on the [GitHub repository](https://github.com/smartmind-team/thanosql-magic).

## License

[MIT](LICENSE)


