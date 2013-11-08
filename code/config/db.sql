
create database validator;

use validator;

create table uploaded_sets (
    id int auto_increment primary key,
    php_session text,
    last_touched int
);

create table uploaded_files (
    id int auto_increment primary key,
    upload_set int,
    filename text,
    document text,
    cached_parse text
);

# install the test/demo file referenced in the help section
insert into uploaded_files values(
    -1,
    -1,
    "test_html_file.html",
    "PCFET0NUWVBFIGh0bWw+DQoNCjxodG1sPjxoZWFkPjwvaGVhZD4NCiANCjxib2R5Pg0KPGgyPkkgYmV0IEkgY2FuIHNuZWFrIGluIGEgbG93ZXIgaGVhZGVyLi4uIG9yIG1heWJlIG5vdCE8L2gyPg0KPGgxPkxvb2sgYXQgdGhlIG1hamVzdHkgb2YgbXkgbXVsdGlwbGUgaGVhZGluZyBvbmVzISE8L2gxPg0KPGgxPldhaXQgdGhhdCdzIGEgYmFkIHRoaW5nPC9oMT4NCjxmcmFtZT5JIGNhbiB1c2UgZnJhbWVzLCByaWdodD88L2ZyYW1lPg0KPHA+RGFuZywgd2hhdCBhYm91dCBsZWF2aW5nIGEgdGFnIMO2cGVuLCB3aXRoIGEgaW1hZ2UgPGltZyBzcmM9IiI+IGFuZCBubyBhbHQgdGV4dCENCjwvYm9keT4NCg0KPC9odG1sPg==",
    "[[62,46,49,{\"name\":\"h2\",\"missing\":\"h1\"}],[41,200,206,{\"name\":\"frame\"}],[41,231,238,{\"name\":\"frame\"}],[51,294,305,{\"name\":\"img\"}],[50,-1,-1,{}],[61,167,170,{\"name\":\"h1\"}],[56,240,242,{\"name\":\"p\"}],[63,-1,-1,{}]]"
);

delimiter //

create procedure garbage_collect()
begin
    create temporary table old_sets(id int);
    insert into old_sets select id from uploaded_sets where last_touched < (unix_timestamp(now())-3600); # 1 hour
    delete from uploaded_files where upload_set in (select id from old_sets);
    delete from uploaded_sets where id in (select id from old_sets);
    drop table old_sets;
end //

create procedure touch_set(in set_id int)
begin
   declare right_now int;
   select unix_timestamp(now()) into right_now;
   update uploaded_sets set last_touched = right_now where id = set_id and last_touched < right_now;
end //

create procedure touch_file(in file_id int)
begin
   call touch_set( (select upload_set from uploaded_files where id = file_id) );
end //

create procedure create_set(in php_session text)
begin
    insert into uploaded_sets values (0, php_session, unix_timestamp(now()));
    select last_insert_id();
end //

create procedure add_file(in upload_set int, in filename text, in document text, in cached_parse text)
begin
    insert into uploaded_files values (0, upload_set, filename, document, cached_parse);
    call touch_set(upload_set);
    select last_insert_id();
end //

create procedure cache_parse(in file int, in parse_data text) 
begin
    update uploaded_files set cached_parse = parse_data where id = file;
    call touch_file(file);
end //

create procedure get_file(in file int)
begin
    call touch_file(file);
    select * from uploaded_files where id = file;
end //

create procedure get_set(in set_id int)
begin
    call touch_set(set_id);
    select id, filename, cached_parse from uploaded_files where upload_set = set_id;
end //

delimiter ;

grant all on validator.* to ''@'localhost';
