"""
All bill-related data functions are contained within this module.

Functions:
    get_bill_json: for <Bill /> objects

Modules:
    database: for the get_cursor function that returns an opened database cursor
    flask for jsonify: so our results return to React in a nice JSON package
"""
from database import get_cursor
from flask import jsonify

def get_bill_json(votequestion_id):

    """
    Returns the JSON data for information on a single specific bill within a politician's profile.
    Is requested as the <Profile /> component is built in React.

    Related React.js component: <Bill />


    :param votequestion_id: votequestion_id that corresponds to the single bill requested

    :return: a jsonify'd dictionary with all the desired bill information
    """
    # get the cursor
    cursor = get_cursor()

    query = (
        "SELECT b.vote, c.party_id, p.name "
        "FROM bills_membervote b, core_electedmember c, core_party p "
        "WHERE b.politician_id = c.politician_id "
        "AND c.party_id = p.id "
        "AND b.votequestion_id = (%s) "
        "ORDER BY c.party_id "
    )

    # If any parameters are used in the above query, insert them in the parameters tuple
    # Insert parameters in the order used in the query unless using %(name)s placeholders
    # see http://initd.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries for more information
    parameters = (votequestion_id,)

    # Execute query
    cursor.execute(query, parameters)

    # Fetch results
    bill_results = cursor.fetchall()

    cy,cn,ca = 0,0,0
    ny,nn,na = 0,0,0
    ly,ln,la = 0,0,0
    by,bn,ba = 0,0,0
    gy,gn,ga = 0,0,0

    partyvotes = [[0 for x in range(30) for x in range(3)]

    for i in range(0,len(bill_results)):
        party_col = bill_results[i]['party_id']
        if bill_results[i]['vote'] == 'Y':
                partyvotes[party_col][0] += 1
        if bill_results[i]['vote'] == 'N':
                partyvotes[party_col][1] += 1
        if bill_results[i]['vote'] == 'A':
                partyvotes[party_col][2] += 1


    print  partyvotes

    # return a JSON response to React (includes header, no extra work needed)
    return jsonify(results=bill_results)
