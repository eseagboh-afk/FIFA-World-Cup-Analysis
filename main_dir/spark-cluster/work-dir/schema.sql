drop schema if exists world_cup cascade;
create schema world_cup;
set search_path to world_cup;

-- Matches Table --

create table matches(
	match_id serial primary key, 
	match_date date not null,
	country_1 varchar(150)not null,
	country_2 varchar(150)not null,
	country_1_score int not null, 
	country_2_score int not null,
	winning_team varchar(150) null,
	losing_team varchar(150) null);

-- Countries Table

create table countries(
	country_id serial primary key, 
	country_name varchar(150) not null, 
	total_matches_played int not null,
	total_matches_won int not null, 
	total_matches_lost int not null, 
	total_goals_scored int not null);

-- Economic Status Table

create table economic_status(
	economic_record_id serial primary key, 
	country_id int not null references countries(country_id),
	avg_total_gdp float null,
	avg_international_liquidity float null, 
	avg_population float null);

-- Winners Table

create table winners(
	winner_id serial primary key, 
	match_id int not null references matches(match_id));

-- Losers Table

create table losers(
	loser_id serial primary key,
	match_id int not null references matches(match_id));

