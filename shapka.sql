PGDMP      %                |            shopdb    16.4    16.4     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16398    shopdb    DATABASE     z   CREATE DATABASE shopdb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE shopdb;
                postgres    false            �            1259    16417    hats    TABLE     b  CREATE TABLE public.hats (
    id_hat integer NOT NULL,
    title character varying(256),
    category character varying(100),
    sex character varying(100),
    season character varying(100),
    ears character varying(100),
    material character varying(100),
    composition character varying(100),
    ties text,
    size character varying(100)
);
    DROP TABLE public.hats;
       public         heap    postgres    false            �            1259    16416    hats_id_hat_seq    SEQUENCE     �   CREATE SEQUENCE public.hats_id_hat_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.hats_id_hat_seq;
       public          postgres    false    216            �           0    0    hats_id_hat_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.hats_id_hat_seq OWNED BY public.hats.id_hat;
          public          postgres    false    215            �            1259    16442    orders    TABLE     �   CREATE TABLE public.orders (
    id_order integer NOT NULL,
    product_name character varying(255) NOT NULL,
    order_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    phone character varying(15)
);
    DROP TABLE public.orders;
       public         heap    postgres    false            �            1259    16441    orders_id_order_seq    SEQUENCE     �   CREATE SEQUENCE public.orders_id_order_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.orders_id_order_seq;
       public          postgres    false    218            �           0    0    orders_id_order_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.orders_id_order_seq OWNED BY public.orders.id_order;
          public          postgres    false    217            U           2604    16420    hats id_hat    DEFAULT     j   ALTER TABLE ONLY public.hats ALTER COLUMN id_hat SET DEFAULT nextval('public.hats_id_hat_seq'::regclass);
 :   ALTER TABLE public.hats ALTER COLUMN id_hat DROP DEFAULT;
       public          postgres    false    216    215    216            V           2604    16445    orders id_order    DEFAULT     r   ALTER TABLE ONLY public.orders ALTER COLUMN id_order SET DEFAULT nextval('public.orders_id_order_seq'::regclass);
 >   ALTER TABLE public.orders ALTER COLUMN id_order DROP DEFAULT;
       public          postgres    false    217    218    218            �          0    16417    hats 
   TABLE DATA           m   COPY public.hats (id_hat, title, category, sex, season, ears, material, composition, ties, size) FROM stdin;
    public          postgres    false    216   @       �          0    16442    orders 
   TABLE DATA           K   COPY public.orders (id_order, product_name, order_date, phone) FROM stdin;
    public          postgres    false    218   �       �           0    0    hats_id_hat_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.hats_id_hat_seq', 234, true);
          public          postgres    false    215            �           0    0    orders_id_order_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.orders_id_order_seq', 20, true);
          public          postgres    false    217            Y           2606    16424    hats hats_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.hats
    ADD CONSTRAINT hats_pkey PRIMARY KEY (id_hat);
 8   ALTER TABLE ONLY public.hats DROP CONSTRAINT hats_pkey;
       public            postgres    false    216            [           2606    16448    orders orders_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id_order);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public            postgres    false    218            �   ;  x��]�r�6�l?��_3�!(�����vrIn����3�I��ܦ3��;%�lŎ�W ߨ���(���;������v!1H�r,���k9����ѱ�Y����y��p�=t �S�U.�W�+=�?\-���g�J.��7�����iuV�Wo��Ky_���p��AV��ɡ�,a�S�.��G��r�����x����U�8G�:�$�G�?�@�e Y�����#�>=�M|H��ɔ෋����̡,j�VWyH��#����Z�=��:Ҁ��#g$���-�Ǉ��0����9��� �����~~0(O2'�q��$KA�"�8�T�IV�0�}&OO��)�E��h/�IH3Fo�'Y	�D7okэ��IO2\��>�`ψ*�iF�^J����2~����cB�20��y:�5AG�/x��Iք=�<C,YH���"kB��u@�UdMpп��&���PM�W� �SdM�V�p��5Y=K@^RdM�U��kyDL$(rѿ�C��<X�T�{���������"����1� �vy���)� X���A�<�e��`�e]vE���.��"X�!�D�}�Џ�ܽ��` �A��"���Π�.=�;(�A�K��``��=vzD�]�[�D����@�%��aT�bh���7�A�7Xv�pb�S�Ls��K�nn�u�%H7y�f�PE(�8�W�8ЬWe`ֈ�2,k�U�5����%`�T�q
qU�	[5⪌��-�Cc�^&t����1��u
J�10�5Îz#=5b.=5b9=5bD=5bO=5bZ}�T�(�)�Y���@�����F�]�Σ�It��)�4��:��&�aW'��$:��[�D�^�~K���3qi~uR.M���ϥIt֩�4���b_P��ބ�a����������TA/���p໺`=��c��	>;�Ϗ�\�:��g��Q�~�ޔ���c�'�Ouv�_��Sy��LQu��`�sl+��r\����#����XXx�@�c�p������H*/�v��/5i+��d��u�|�5	��̫` 5�C���b>%��_��Mx�@�ߨ�����c��m���!BM=s��->����l�6�ޏ�_5���l�@��٨���q!��`���쌁{`��56�QC��k�Ffh��+"��T��o�W��s͢�iK����P���-ۯ�up�F�<^�8Ц� C���Ͷ^���i���9���w|�^��f�/{�z����*�Z+T�76*���G�������>��U�{m�����mdz}S�7���m��p��~�`-&Ky´�	��W��lZ�تHm���_���C���YŁ�,�B���ങV|e�����|Z��Ҳ��St$k-������ge �{`�y�:���)��[I.w����m>���"	���c��\�{�p��c����@_�[�44�QT�_��� �'�/��۔+��^�4j�|~���b�|7	|��3�P�(��S�Ԣ��`��n�6���;��n��'�O'�t��]��ݹڍ�����W[b[ǵIg8��h���b��ќG�M������:��`�%�sm_o�����-;��mۭ]�;ݹ��- �˂���� z���#�0w�ݼ}��(��uM��#vl��^�X���m�M�0�ىM�u�!5  l)��o~�ؠ��:J���#w,�M��tȏ�,3Z)��~v�}�2
OW�1���c�ռ����#�ԝ�13�,�A�)�]�W�q�� ���;�W�ߘI�,spɗ
�������Z����I��&��|���!�����[��8|�Wj?�k��=GV��FjY)}@ԑ�y�qd�������m���3�}?�'r?o� �=��eeC�?̵}���0!Xs��G�˾a�k�ֲ�r�k'��'o�@9�P���K�����40-�35�^���Q��
qyn�9y�MhzA-���'�|W$BEuA�>��兓H�Up�U��QV����1d�+�L�vY���q-Pn!�;�b0n#3�	FD��'��bQ#��䈶��Ү��ϙi�q*�;�.�w��M:7_a��-�R����&@���E��B�(c��K�^Ҷ(F������@4.�B2�f�b_��������qw��{ᩑ���Z���jPD��<���)a�-�&��/�	g4�=|�M���DV���O�uVv�i��K6ԃ@�����JO���d��:�ي[�2����_WH�Է��lX؎qF���s��h/�G��8v$\;<?`<(ͤ�>��"��
ZG����{�@��h#.�Z|+L{���F%[Q~����:���'>��
:gk�j�-+-"�[��y)3�V�3v�������፞�8�Uh=��������
C;r��ްrh����س���tj��".8����r��);~x'�27}��l�#ǩ�86����ǵT�S�٧�n9k;����:ٽ8�5�xƱ^�΃;��Z�j�9!8�D����S�uE�Bz��w�I�nO�{��H<�3?����
u�[oOZn��e`f6K���lC���\�2�$����GR�2�k���N�(�(�{BҜ:��#������ƹ�g�[❯h���-��x����z�Vi�Z8����
7wES�P�%���k�	��b�9m�[Y��(C�,Ą�H���3�GC���G�^c��ǟ�D��uz��ȇTB��˵���TC��>1��B8��=G0��0w�	�Dt��q]�ZV#}*Rh�~\�g~�(g�5�����ؙg�0yز-���I�<�� ��M�V=w�D�ν�|��i9`pX���p|��ZL��[���$������'cD9i��-��?TS+�*��K�K�S�����	��#.�FMG'���F�߮��OP
�A�m�]+���QD�jQ��юIc��ڊE��5�w]�;D���(�ɳqã}�C4q�oߎ+#Z�]��_�l4�cH������`�75      �     x���=N1�k�{�X���@GO�q�(� 		$�܈Y�6�D�<��o�<�ɐ)aE�U�U�;j/*M9=�gL@~�P�#� ���!8��f�`d�eE�"�+�aK���t�V�4^���o�x�+�h8{����O�5k��&�bIU3�����{QKk��%$�XBmI�\@��
�0��8��ʹ,C���;XQta@�+���彶�bl��no����!C�G�m�Q_~��u�\�$�<>���ߞ���ĝ���9��<5�I���Xr�?�C��     