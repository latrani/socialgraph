drop table if exists auth_users;
create table auth_users (
	id integer primary key autoincrement,
	username text unique not null,
	hashword text not null,
	salt integer not null,
	email text not null,
	display_name text,
	is_staff integer default 0,
	is_admin integer default 0
);
create unique index user_login_idx ON auth_users(username, salt, hashword);

drop table if exists graph;
create table graph (
	id integer primary key autoincrement,
	user_id integer,
	foreign key(user_id) references auth_users(id)
);

drop table if exists vertex;
create table vertex (
	id integer primary key autoincrement,
	graph_id integer not null,
	name text not null,
	user_id integer,
	foreign key(graph_id) references graph(id),
	foreign key(user_id) references auth_users(id)
);

drop table if exists edge;
create table edge (
	id integer primary_key autoincrement,
	source_id integer not null,
	target_id integer not null,
	edge_type text not null,
	source_meaning text,
	target_meaning text,
	center_meaning text
	ex boolean not null default false,
	foreign key(source_id) references vertex(id),
	foreign key(target_id) references vertex(id)
)a;
