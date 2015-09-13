"""
All bill-related data functions are contained within this module.

Functions:
    get_bill_json: for <Bill /> objects

Modules:
    database: for the cursor object
    flask for jsonify: so our results return to React in a nice JSON package
"""
from database import cursor
from flask import jsonify

def get_bill_json(votequestion_id, cursor=cursor):

    """
    Returns the JSON data for information on a single specific bill within a politician's profile.
    Is requested as the <Profile /> component is built in React.

    Related React.js component: <Bill />


    :param votequestion_id: votequestion_id that corresponds to the single bill requested

    :param bill_id: id of the single bill requested

    :param cursor: current database cursor - no need to supply this or change this from the default
    :return: a jsonify'd dictionary with all the desired bill information
    """
    # <SHAY> BUILD THIS QUERY
    # Build our query with all the desired relevant info we want to display about bills.
    # Add any parameters using (%s) or (%(name)s). More information below.
    query = (
        "SELECT number,name_en,law,short_title_en,institution "
        "FROM bills_bill "
        "WHERE id = "
        "("
            "SELECT bill_id "
            "FROM bills_votequestion "
            "WHERE id = (%s)"
        ")"
    )


    # If any parameters are used in the above query, insert them in the parameters tuple
    # Insert parameters in the order used in the query unless using %(name)s placeholders
    # see http://initd.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries for more information
    parameters = (votequestion_id,)

    # Execute query
    cursor.execute(query, parameters)

    # Fetch results
    bill_results = cursor.fetchall()

    # return a JSON response to React (includes header, no extra work needed)
    return jsonify(results=bill_results)
