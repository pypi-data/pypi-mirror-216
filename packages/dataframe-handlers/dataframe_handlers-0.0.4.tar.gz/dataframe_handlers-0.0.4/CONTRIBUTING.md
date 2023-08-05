This `CONTRIBUTING.md` was produced by [OpenAI's _gpt-3.5-turbo_](https://platform.openai.com/docs/models/gpt-3-5).

# Contributing to `dataframe_handlers`

Thank you for your interest in contributing to `dataframe_handlers`! This guide outlines the steps required to integrate a new handler into the library. By following these instructions, you can extend the functionality of `dataframe_handlers` and enable interoperability with additional dataframe libraries.

## Integrating a New Handler

To integrate a new handler, you need to create a concrete implementation of the base handler class and a corresponding test class. These steps will guide you through the process:

1. **Fork the Repository**: Start by forking the `dataframe_handlers` repository to your GitHub account. You can do this by clicking the "Fork" button on the repository page.

2. **Create a New Branch**: Clone the forked repository to your local development environment. Create a new branch with a descriptive name that reflects the purpose of your contribution.

   ```bash
   git clone https://github.com/your-username/dataframe_handlers.git
   cd dataframe_handlers
   git checkout -b my_library_handler
   ```

3. **Implement the Handler**: Create a new Python module within the `dataframe_handlers` package to contain your handler implementation.

   ```text
    dataframe_handlers/
        my_library_handler/
            my_library_handler.py
            __init__.py
    tests/
        test_my_library_handler.py
   ```

   <br>

   In the new module, define a concrete class that inherits from the `BaseDataFrameHandler` class. This new class should override the necessary methods to provide functionality specific to the `my_library` dataframe library. Use the existing handlers, such as the `PandasDataFrameHandler`, as a reference for implementing the required methods. Make sure to import the necessary dependencies.

   ```python
   # Example: dataframe_handlers/my_library_handler/my_library_handler.py

   import my_library

   from ..base import BaseDataFrameHandler

   # you can also inherit from an existing handler
   # for example if the methods of `my_library` are mostly similar to pandas,
   # inherit the pandas handler and override methods only as needed
   # see the dask handler for an example of this

   class MyLibraryDataFrameHandler(BaseDataFrameHandler):
       df: my_library.DataFrame

       # Implement the necessary methods here
       # ...
   ```

   <br>

   ```python
   # Example: dataframe_handlers/my_library_handler/__init__.py

   from .my_library_handler import MyLibraryDataFrameHandler

   __all__ = ["MyLibraryDataFrameHandler"]
   ```

4. **Implement the Test Class**: Create a new Python module within the `tests` directory to contain your test class. For consistency, name the file `test_my_library_handler.py`.

   In the new module, define a test class that inherits from the `DataFrameHandlerTestBase` class. Override the `data` fixture to return a dataframe from the `my_library` library that you want to use for testing. You can follow the example of the Pandas test class and return a dataframe with the same data structure.

   ```python
   # Example: tests/test_my_library_handler.py

   import pytest
   import my_library

   from . import DataFrameHandlerTestBase, test_pandas_df

   class TestMyLibraryDataFrameHandler(DataFrameHandlerTestBase):
       @pytest.fixture
       def data(self):
           # Return a dataframe from the my_library library for testing
           # This assumes you can construct a `my_libary.DataFrame` given a pandas DataFrame
           return my_library.DataFrame(test_pandas_df)
   ```

5. **Update `README.md`**: If you have created a new handler that supports a new library, update the `README.md` file to include the new library in the list of supported implementations. Provide documentation and instructions as appropriate.

6. **Run Tests**: Before submitting your contribution, make sure to run the tests locally to verify that your new handler works correctly. Execute the following command from the root of the `dataframe_handlers` repository:

   ```bash
   # install pre-commit, update hooks
   pip install pre-commit
   pre-commit install
   pre-commit autoupdate

   # ...fix things... or break things...

   # run tests, create coverage report
   docker compose run tester

   # or run the tests manually by some other means
   # feel free to reach out for assistance with pre-commit, checks, and testing

   # add your changes, run pre-commit until everything passes
   git add -u && pre-commit run
   ```

   <br>

   Ensure that all checks and tests pass with high coverage of your new handler and without any failures or errors.

7. **Commit and Push Changes**: Once your implementation and tests are complete, commit your changes and push them to your forked repository.

   ```bash
   git add .
   git commit -m "Add MyLibraryDataFrameHandler implementation"
   git push origin my_library_handler
   ```

8. **Create a Pull Request**: Go to the dataframe_handlers repository on GitHub and switch to the branch you pushed. Click the "New Pull Request" button to create a pull request for the associated branch.

   1. Compare Across Forks: On the page to create a new pull request, click on the "compare across forks" link. This allows you to compare and merge your changes from the forked repository to the original repository.

   2. Select Base and Compare Branches: In the "base branch" dropdown menu, select the branch of the upstream repository you'd like to merge changes into. In the "head fork" dropdown menu, select your fork, and then use the "compare branch" dropdown menu to select the branch you made your changes in.

   3. Provide Title and Description: Type a title and description for your pull request. Provide a clear and concise summary of the changes you've made.

   4. Create the Pull Request: To create a pull request that is ready for review, click "Create Pull Request". This will open the pull request in the upstream repository.

9. **Review and Iterate**: Your pull request will be reviewed by the project maintainers. They may provide feedback or request changes. Be responsive to the feedback and make any necessary updates or improvements based on the review comments. Iterate on this process until your contribution is accepted.

<br>

Congratulations! You have successfully integrated a new handler into the `dataframe_handlers` library. Your contribution will enable users to work with dataframes from the `my_library` library seamlessly using the standardized interface.

---

Thank you for your contribution to `dataframe_handlers`! We appreciate your effort in expanding the library's functionality and supporting additional dataframe libraries. If you have any questions or need further assistance, don't hesitate to reach out to the project maintainers.

Happy coding!

*Note: Make sure to replace the placeholders (`my_library`, `MyLibraryDataFrameHandler`, etc.) with the appropriate names based on the library you are integrating and the specific class and module names you choose for your implementation.*
