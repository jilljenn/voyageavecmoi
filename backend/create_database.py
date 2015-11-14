import rethinkdb as r

def bulk_create_db(db_names):
    c = r.connect("localhost", 28015)
    for db_name in db_names:
        r.db_create(db_name).run(c)
        print ('BDD `{}` créée.'.format(db_name))
    print ('Toutes les base de données ont été crées.')

def bulk_create_tables(db_name, table_names):
    c = r.connect("localhost", 28015, db=db_name)
    for table in table_names:
        r.table_create(table).run(c)
        print ('Table `{}` créée.'.format(table))
    print ('Toutes les tables ont été crées')

db_names = ['voyageavecmoi']
tables = {
    'voyageavecmoi': ['offers']
}
print ('Je vais commencer à créer la DB pour utiliser le backend!')
bulk_create_db(db_names)
for db_name, tables in tables.items():
    bulk_create_tables(db_name, tables)

print ('Base de données prête!')
