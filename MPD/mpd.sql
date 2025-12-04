/*==============================================================*/
/* Nom de SGBD :  PostgreSQL 9.x                                */
/* Date de cr�ation :  04/12/2025 20:46:48                      */
/*==============================================================*/




/*==============================================================*/
/* Table : BATIMENT                                             */
/*==============================================================*/
create table BATIMENT (
   CODE_BATIMENT        INT4                 not null,
   ID_ZONE              INT4                 not null,
   ID_TYPE              INT4                 not null,
   ID_PROTECTION        INT4                 not null,
   ID_PROPRIO           INT4                 not null,
   NOM_BATIMENT         CHAR(50)             null,
   ADRESSE              CHAR(150)            null,
   LATITUDE             DECIMAL              null,
   LONGITUDE            DECIMAL              null,
   DATE_CONSTRUCTION    DATE                 null,
   NOTE_HISTORIQUE      TEXT                 null,
   constraint PK_BATIMENT primary key (CODE_BATIMENT)
);



/*==============================================================*/
/* Table : DOCUMENT___MEDIA                                     */
/*==============================================================*/
create table DOCUMENT___MEDIA (
   ID_DOC               INT4                 not null,
   CODE_BATIMENT        INT4                 not null,
   TITRE_DOCUMENT       CHAR(50)             null,
   TYPE                 CHAR(20)             null,
   URL_FICHIER          CHAR(200)            null,
   constraint PK_DOCUMENT___MEDIA primary key (ID_DOC)
);


/*==============================================================*/
/* Table : INSPECTION                                           */
/*==============================================================*/
create table INSPECTION (
   ID_INSPECT           INT4                 not null,
   CODE_BATIMENT        INT4                 not null,
   DATE_VISITE          DATE                 null,
   ETAT                 CHAR(20)             null,
   constraint PK_INSPECTION primary key (ID_INSPECT)
);


/*==============================================================*/
/* Table : INTERVENTION                                         */
/*==============================================================*/
create table INTERVENTION (
   ID_INTERV            INT4                 not null,
   CODE_BATIMENT        INT4                 not null,
   ID_PRESTATAIRE       INT4                 not null,
   DATE_DEBUT           DATE                 null,
   TYPE_TRAVAUX         CHAR(20)             null,
   COUT_ESTIME          MONEY                null,
   constraint PK_INTERVENTION primary key (ID_INTERV)
);





/*==============================================================*/
/* Table : NIV_PROTECTION                                       */
/*==============================================================*/
create table NIV_PROTECTION (
   ID_PROTECTION        INT4                 not null,
   NIVEAU               CHAR(20)             null,
   constraint PK_NIV_PROTECTION primary key (ID_PROTECTION)
);



/*==============================================================*/
/* Table : PRESTATAIRE                                          */
/*==============================================================*/
create table PRESTATAIRE (
   ID_PRESTATAIRE       INT4                 not null,
   NOM_ENTREPRISE       CHAR(50)             null,
   ROLE                 CHAR(50)             null,
   constraint PK_PRESTATAIRE primary key (ID_PRESTATAIRE)
);



/*==============================================================*/
/* Table : PROPRIETAIRE                                         */
/*==============================================================*/
create table PROPRIETAIRE (
   ID_PROPRIO           INT4                 not null,
   NOM                  CHAR(50)             null,
   CONTACT              NUMERIC              null,
   constraint PK_PROPRIETAIRE primary key (ID_PROPRIO)
);



/*==============================================================*/
/* Table : TYPE_BATIMENT                                        */
/*==============================================================*/
create table TYPE_BATIMENT (
   ID_TYPE              INT4                 not null,
   LIBELLE_TYPE         CHAR(50)             null,
   constraint PK_TYPE_BATIMENT primary key (ID_TYPE)
);



/*==============================================================*/
/* Table : ZONE_URBAINE                                         */
/*==============================================================*/
create table ZONE_URBAINE (
   ID_ZONE              INT4                 not null,
   NOM_ZONE             CHAR(50)             null,
   constraint PK_ZONE_URBAINE primary key (ID_ZONE)
);

