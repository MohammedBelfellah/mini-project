/*==============================================================*/
/* Nom de SGBD :  PostgreSQL 9.x                                */
/* Date de cr�ation :  04/12/2025 18:58:29                      */
/*==============================================================*/


drop index APPARTENIR_FK;

drop index ETRE_PROTEGE_FK;

drop index AVOIR_TYPE_FK;

drop index SE_SITUER_FK;

drop index BATIMENT_PK;

drop table BATIMENT;

drop index ILLUSTRER_FK;

drop index DOCUMENT___MEDIA_PK;

drop table DOCUMENT___MEDIA;

drop index FAIRE_L_OBJET_FK;

drop index INSPECTION_PK;

drop table INSPECTION;

drop index SUBIR_TX_FK;

drop index INTERVENTION_PK;

drop table INTERVENTION;

drop index NIV_PROTECTION_PK;

drop table NIV_PROTECTION;

drop index PRESTATAIRE_PK;

drop table PRESTATAIRE;

drop index PROPRIETAIRE_PK;

drop table PROPRIETAIRE;

drop index REALISER_FK;

drop index REALISER2_FK;

drop index REALISER_PK;

drop table REALISER;

drop index TYPE_BATIMENT_PK;

drop table TYPE_BATIMENT;

drop index ZONE_URBAINE_PK;

drop table ZONE_URBAINE;

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
/* Index : BATIMENT_PK                                          */
/*==============================================================*/
create unique index BATIMENT_PK on BATIMENT (
CODE_BATIMENT
);

/*==============================================================*/
/* Index : SE_SITUER_FK                                         */
/*==============================================================*/
create  index SE_SITUER_FK on BATIMENT (
ID_ZONE
);

/*==============================================================*/
/* Index : AVOIR_TYPE_FK                                        */
/*==============================================================*/
create  index AVOIR_TYPE_FK on BATIMENT (
ID_TYPE
);

/*==============================================================*/
/* Index : ETRE_PROTEGE_FK                                      */
/*==============================================================*/
create  index ETRE_PROTEGE_FK on BATIMENT (
ID_PROTECTION
);

/*==============================================================*/
/* Index : APPARTENIR_FK                                        */
/*==============================================================*/
create  index APPARTENIR_FK on BATIMENT (
ID_PROPRIO
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
/* Index : DOCUMENT___MEDIA_PK                                  */
/*==============================================================*/
create unique index DOCUMENT___MEDIA_PK on DOCUMENT___MEDIA (
ID_DOC
);

/*==============================================================*/
/* Index : ILLUSTRER_FK                                         */
/*==============================================================*/
create  index ILLUSTRER_FK on DOCUMENT___MEDIA (
CODE_BATIMENT
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
/* Index : INSPECTION_PK                                        */
/*==============================================================*/
create unique index INSPECTION_PK on INSPECTION (
ID_INSPECT
);

/*==============================================================*/
/* Index : FAIRE_L_OBJET_FK                                     */
/*==============================================================*/
create  index FAIRE_L_OBJET_FK on INSPECTION (
CODE_BATIMENT
);

/*==============================================================*/
/* Table : INTERVENTION                                         */
/*==============================================================*/
create table INTERVENTION (
   ID_INTERV            INT4                 not null,
   CODE_BATIMENT        INT4                 not null,
   DATE_DEBUT           DATE                 null,
   TYPE_TRAVAUX         CHAR(20)             null,
   COUT_ESTIME          MONEY                null,
   constraint PK_INTERVENTION primary key (ID_INTERV)
);

/*==============================================================*/
/* Index : INTERVENTION_PK                                      */
/*==============================================================*/
create unique index INTERVENTION_PK on INTERVENTION (
ID_INTERV
);

/*==============================================================*/
/* Index : SUBIR_TX_FK                                          */
/*==============================================================*/
create  index SUBIR_TX_FK on INTERVENTION (
CODE_BATIMENT
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
/* Index : NIV_PROTECTION_PK                                    */
/*==============================================================*/
create unique index NIV_PROTECTION_PK on NIV_PROTECTION (
ID_PROTECTION
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
/* Index : PRESTATAIRE_PK                                       */
/*==============================================================*/
create unique index PRESTATAIRE_PK on PRESTATAIRE (
ID_PRESTATAIRE
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
/* Index : PROPRIETAIRE_PK                                      */
/*==============================================================*/
create unique index PROPRIETAIRE_PK on PROPRIETAIRE (
ID_PROPRIO
);

/*==============================================================*/
/* Table : REALISER                                             */
/*==============================================================*/
create table REALISER (
   ID_INTERV            INT4                 not null,
   ID_PRESTATAIRE       INT4                 not null,
   constraint PK_REALISER primary key (ID_INTERV, ID_PRESTATAIRE)
);

/*==============================================================*/
/* Index : REALISER_PK                                          */
/*==============================================================*/
create unique index REALISER_PK on REALISER (
ID_INTERV,
ID_PRESTATAIRE
);

/*==============================================================*/
/* Index : REALISER2_FK                                         */
/*==============================================================*/
create  index REALISER2_FK on REALISER (
ID_INTERV
);

/*==============================================================*/
/* Index : REALISER_FK                                          */
/*==============================================================*/
create  index REALISER_FK on REALISER (
ID_PRESTATAIRE
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
/* Index : TYPE_BATIMENT_PK                                     */
/*==============================================================*/
create unique index TYPE_BATIMENT_PK on TYPE_BATIMENT (
ID_TYPE
);

/*==============================================================*/
/* Table : ZONE_URBAINE                                         */
/*==============================================================*/
create table ZONE_URBAINE (
   ID_ZONE              INT4                 not null,
   NOM_ZONE             CHAR(50)             null,
   constraint PK_ZONE_URBAINE primary key (ID_ZONE)
);

/*==============================================================*/
/* Index : ZONE_URBAINE_PK                                      */
/*==============================================================*/
create unique index ZONE_URBAINE_PK on ZONE_URBAINE (
ID_ZONE
);

alter table BATIMENT
   add constraint FK_BATIMENT_APPARTENI_PROPRIET foreign key (ID_PROPRIO)
      references PROPRIETAIRE (ID_PROPRIO)
      on delete restrict on update restrict;

alter table BATIMENT
   add constraint FK_BATIMENT_AVOIR_TYP_TYPE_BAT foreign key (ID_TYPE)
      references TYPE_BATIMENT (ID_TYPE)
      on delete restrict on update restrict;

alter table BATIMENT
   add constraint FK_BATIMENT_ETRE_PROT_NIV_PROT foreign key (ID_PROTECTION)
      references NIV_PROTECTION (ID_PROTECTION)
      on delete restrict on update restrict;

alter table BATIMENT
   add constraint FK_BATIMENT_SE_SITUER_ZONE_URB foreign key (ID_ZONE)
      references ZONE_URBAINE (ID_ZONE)
      on delete restrict on update restrict;

alter table DOCUMENT___MEDIA
   add constraint FK_DOCUMENT_ILLUSTRER_BATIMENT foreign key (CODE_BATIMENT)
      references BATIMENT (CODE_BATIMENT)
      on delete restrict on update restrict;

alter table INSPECTION
   add constraint FK_INSPECTI_FAIRE_L_O_BATIMENT foreign key (CODE_BATIMENT)
      references BATIMENT (CODE_BATIMENT)
      on delete restrict on update restrict;

alter table INTERVENTION
   add constraint FK_INTERVEN_SUBIR_TX_BATIMENT foreign key (CODE_BATIMENT)
      references BATIMENT (CODE_BATIMENT)
      on delete restrict on update restrict;

alter table REALISER
   add constraint FK_REALISER_REALISER_PRESTATA foreign key (ID_PRESTATAIRE)
      references PRESTATAIRE (ID_PRESTATAIRE)
      on delete restrict on update restrict;

alter table REALISER
   add constraint FK_REALISER_REALISER2_INTERVEN foreign key (ID_INTERV)
      references INTERVENTION (ID_INTERV)
      on delete restrict on update restrict;

