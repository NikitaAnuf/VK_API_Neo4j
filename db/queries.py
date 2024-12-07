from db.connection import Connection


def add_followers(user: dict, follower: dict) -> None:
    session = Connection.session
    session.run(
        "MERGE (user:User {id: $id, screen_name: $screen_name, name: $name, sex: $sex, home_town: $home_town})"
        "MERGE (follower:User {id: $fid, screen_name: $fscreen_name, name: $fname, sex: $fsex, home_town: $fhome_town})"
        "MERGE (follower)-[:FOLLOW]->(user)",
        id=user['id'], screen_name=user['screen_name'], name=user['name'], sex=user['sex'], home_town=user['home_town'],
        fid=follower['id'], fscreen_name=follower['screen_name'], fname=follower['name'], fsex=follower['sex'],
        fhome_town=follower['home_town']
    )


def add_subscription_users(user: dict, subscription: dict) -> None:
    session = Connection.session
    session.run(
        "MERGE (user:User {id: $id, screen_name: $screen_name, name: $name, sex: $sex, home_town: $home_town})"
        "MERGE (subscription:User {id: $sid, screen_name: $sscreen_name, name: $sname, sex: $ssex, home_town: $shome_town})"
        "MERGE (user)-[:SUBSCRIBE]->(subscription)",
        id=user['id'], screen_name=user['screen_name'], name=user['name'], sex=user['sex'],
        home_town=user['home_town'], sid=subscription['id'], sscreen_name=subscription['screen_name'],
        sname=subscription['name'], ssex=subscription['sex'], shome_town=subscription['home_town']
    )


def add_subscription_groups(user: dict, subscription: dict) -> None:
    session = Connection.session
    session.run(
        "MERGE (user:User {id: $id, screen_name: $screen_name, name: $name, sex: $sex, home_town: $home_town})"
        "MERGE (subscription:Group {id: $sid, screen_name: $sscreen_name, name: $sname})"
        "MERGE (user)-[:SUBSCRIBE]->(subscription)",
        id=user['id'], screen_name=user['screen_name'], name=user['name'], sex=user['sex'],
        home_town=user['home_town'], sid=subscription['id'], sscreen_name=subscription['screen_name'],
        sname=subscription['name']
    )

def count_users() -> int:
    session = Connection.session
    result = session.run("MATCH (u:User) RETURN COUNT(u)")
    return result.single()[0]


def count_groups() -> int:
    session = Connection.session
    result = session.run("MATCH (g:Group) RETURN COUNT(g)")
    return result.single()[0]


def top_followed_users(n: int) -> list[dict]:
    session = Connection.session
    result = session.run(
        "MATCH (f:User)-[:FOLLOW]->(u:User) RETURN u AS User, COUNT(f) AS number_of_followers ORDER BY number_of_followers DESC LIMIT $n",
        n=n
    )

    res = []
    for line in result:
        line = dict(line)
        line['User'] = dict(line['User'])
        res.append(dict(line))

    return res


def top_subscribed_groups(n: int) -> list[dict]:
    session = Connection.session
    result = session.run(
        "MATCH (u:User)-[:SUBSCRIBE]->(g:Group) RETURN g AS Group, COUNT(u) AS number_of_subscribers ORDER BY number_of_subscribers DESC LIMIT $n",
        n=n
    )

    res = []
    for line in result:
        line = dict(line)
        line['Group'] = dict(line['Group'])
        res.append(line)

    return res


def mutual_followers() -> list[dict]:
    session = Connection.session
    result = session.run("MATCH (f:User)-[:FOLLOW]->(u:User) WHERE (u)-[:FOLLOW]->(f) RETURN f AS User1, u AS User2")

    res = []
    for line in result:
        line = dict(line)
        line['User1'] = dict(line['User1'])
        line['User2'] = dict(line['User2'])
        res.append(line)

    return res
