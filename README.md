# FinTrack

A web application to help you track your personal finances, manage budgets, and gain insights into your spending habits. With a user-friendly interface, powerful filtering options, and budget management, this project makes managing your money simple and effective.

## Live Demo

Check out the live application on Heroku: [Django Finance Project](https://fintrack-pdm-511a83ebf2da.herokuapp.com/)

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Configuration](#configuration)
5. [Technologies Used](#technologies-used)
6. [Contributing](#contributing)
7. [License](#license)
8. [Acknowledgments](#acknowledgments)

## Features

- **Transaction Management**: Add, edit, delete, and view financial transactions.
- **Budget Tracking**: Define budgets with `BudgetItem` models and monitor spending.
- **CSV Uploads**: Easily import transactions from CSV files.
- **Filtering Options**: Filter transactions by predefined or custom date ranges.
- **Dashboard**: Visualize financial insights, including spending summaries and budget performance.
- **Responsive Design**: Built with TailwindCSS for a seamless experience on any device.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd django-finance-project
   ```
3. Install dependencies using `uv`:
   ```bash
   uv sync
   ```
4. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```
6. Access the app at `http://127.0.0.1:8000/`.

## Usage

1. **Add Transactions**: Navigate to the "Transactions" section to add income or expenses.
2. **Filter Transactions**: Use the `filter_form` to view transactions within specific date ranges.
3. **Manage Budgets**: Create and monitor budget items to keep track of your spending goals.
4. **Dashboard**: Get insights into your financial health on the dashboard.
5. **Upload CSV Files**: Import transactions quickly by uploading CSV files in the designated section.

## Configuration

### Environment Variables

Create a `.env` file in the root directory and add the following variables:

```env
SECRET_KEY=<your-secret-key>
DEBUG=True
DATABASE_URL=postgres://<username>:<password>@<host>:<port>/<database>
```

### TailwindCSS

Ensure TailwindCSS is properly configured in your project to apply styles effectively.

## Technologies Used

- **Framework**: Django
- **Database**: PostgreSQL
- **Frontend**: TailwindCSS
- **Project Management**: Astral (`uv`)
- **Deployment**: Heroku
- **Python Version**: 3.13

## Contributing

We welcome contributions! To get started:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [PyBites PDM Program]([https://codechalleng.es/](https://pybit.es/python-certifications/pcpd-p/))
- [Django Documentation](https://docs.djangoproject.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)

---

Feel free to suggest any improvements or share your feedback!

