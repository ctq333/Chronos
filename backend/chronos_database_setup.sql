create table user
(
    id               bigint auto_increment
        primary key,
    username         varchar(64)                        not null,
    password_hash    varchar(255)                       not null,
    status           tinyint  default 1                 null,
    email            varchar(128)                       null,
    created_at       datetime default CURRENT_TIMESTAMP null,
    updated_at       datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    is_admin         tinyint  default 0                 null,
    token            varchar(255)                       null,
    token_expires_at datetime                           null,
    constraint email
        unique (email),
    constraint username
        unique (username)
);

create table monthly_report
(
    id         bigint auto_increment
        primary key,
    user_id    bigint                             not null,
    content    text                               null,
    created_at datetime default CURRENT_TIMESTAMP not null,
    start_date date                               not null,
    end_date   date                               not null,
    constraint monthly_report_ibfk_1
        foreign key (user_id) references user (id)
            on delete cascade
);

create index user_id
    on monthly_report (user_id);

create table schedule
(
    id          bigint auto_increment
        primary key,
    user_id     bigint       not null,
    title       varchar(100) not null,
    description text         null,
    start_time  datetime     not null,
    end_time    datetime     not null,
    location    varchar(255) null,
    link        varchar(255) null,
    constraint schedule_ibfk_1
        foreign key (user_id) references user (id)
            on delete cascade
);

create index user_id
    on schedule (user_id);

create table schedule_invitation
(
    id          bigint auto_increment
        primary key,
    schedule_id bigint                             not null,
    sender_id   bigint                             not null,
    receiver_id bigint                             not null,
    created_at  datetime default CURRENT_TIMESTAMP not null,
    status      tinyint  default 0                 not null comment '0-未处理 1-接收 2-拒绝',
    constraint schedule_invitation_ibfk_1
        foreign key (schedule_id) references schedule (id)
            on delete cascade,
    constraint schedule_invitation_ibfk_2
        foreign key (sender_id) references user (id)
            on delete cascade,
    constraint schedule_invitation_ibfk_3
        foreign key (receiver_id) references user (id)
            on delete cascade
);

create index receiver_id
    on schedule_invitation (receiver_id);

create index schedule_id
    on schedule_invitation (schedule_id);

create index sender_id
    on schedule_invitation (sender_id);

create table task
(
    id             bigint auto_increment
        primary key,
    user_id        bigint                             not null,
    title          varchar(100)                       not null,
    plan_date      date                               not null,
    due_date       date                               not null,
    priority       tinyint  default 2                 null,
    notes          varchar(255)                       null,
    progress       tinyint  default 0                 null,
    status         tinyint  default 0                 null,
    postpone_count int      default 0                 null,
    created_at     datetime default CURRENT_TIMESTAMP null,
    updated_at     datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    tag            varchar(255)                       null,
    constraint task_ibfk_1
        foreign key (user_id) references user (id)
            on delete cascade
);

create table subtask
(
    id             bigint auto_increment
        primary key,
    parent_task_id bigint            not null,
    title          varchar(100)      not null,
    completed      tinyint default 0 null,
    constraint subtask_ibfk_1
        foreign key (parent_task_id) references task (id)
            on delete cascade
);

create index parent_task_id
    on subtask (parent_task_id);

create index user_id
    on task (user_id);

create table weekly_report
(
    id         bigint auto_increment
        primary key,
    user_id    bigint                             not null,
    week       varchar(20)                        not null,
    content    text                               not null,
    created_at datetime default CURRENT_TIMESTAMP null,
    constraint fk_weekly_report_user_id
        foreign key (user_id) references user (id)
            on delete cascade
);

