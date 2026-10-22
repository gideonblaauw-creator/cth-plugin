# Política de privacidad de cleantechhub.net

Borrador del 22 de octubre de 2026. Gideon aprobó preparar este texto. **Awaiting Gideon's approval** antes de publicarlo. No está en el sitio.

El texto público empieza en «Política de privacidad». Lo de arriba es la guía de publicación.

## Cómo está hecho y dónde vive el sitio

Comprobado el 22 de octubre de 2026, sin entrar al administrador.

- Es WordPress. La respuesta de `https://cleantechhub.net/` trae `Link: <https://cleantechhub.net/wp-json/>` y la portada es la página 347.
- El servidor anuncia `Server: Apache`.
- El tema es Astra. La hoja de estilo pública dice versión 4.14.0.
- Las páginas se arman con Elementor. La página Governance tiene el diseño `page-builder`.
- El idioma lo maneja Polylang. Español es el idioma por defecto, en `https://cleantechhub.net/`. Inglés vive bajo `https://cleantechhub.net/en/`. La portada en inglés es `/en/home-english/`.
- El SEO es Rank Math. La API pública incluye la ruta de redirecciones.
- También están visibles GTranslate, WPForms Lite, ElementsKit y Essential Addons.
- Los DNS son `ns10.ovh.ca` y `dns10.ovh.ca`. El registro A es `51.195.42.49`.
- Ese IP cae en el bloque RIPE `VPS-DE2` (`51.195.40.0`–`51.195.43.255`). El titular del bloque es OVH GmbH, en Alemania.
- No se abrió el panel de WordPress ni el servidor. No se publicó nada.

## Dónde publicarla

La URL final es `https://cleantechhub.net/politica-de-privacidad/`.

`/privacy` y `/privacy/` deben redirigir ahí con un 301.

Hoy esas rutas responden 404. El mapa del sitio no tiene una página de privacidad. El pie de página tampoco tiene ese enlace.

## Pasos para publicarla

Hágalo Gideon, o quien administre WordPress. Este borrador no se despliega solo.

1. Confirme el RUT (Registro Único Tributario) y el correo de contacto. No publique mientras esos campos digan `[GIDEON TO FILL]`.
2. Entre a `https://cleantechhub.net/wp-admin/` con su propia cuenta.
3. Vaya a Páginas → Añadir nueva.
4. Título: `Política de privacidad`.
5. Enlace permanente: `politica-de-privacidad`. El sitio ya usa enlaces del tipo `/governance/`, así que la URL queda `https://cleantechhub.net/politica-de-privacidad/`.
6. En Polylang, deje el idioma en Español. Así la página no queda bajo `/en/`. El inglés va dentro de la misma página, después del español.
7. Edite con Elementor. Añada un widget de HTML. Pegue solo el contenido de `<main>` del archivo `artifacts/cleantechhub-privacy-policy.html`. No pegue el comentario de borrador ni el `<style>`.
8. Si la página nueva abre en el editor de bloques, use un bloque HTML personalizado y pegue el mismo `<main>`.
9. Publique. Abra la URL en una ventana privada. Tiene que verse sin iniciar sesión.
10. En Rank Math → Redirections, cree un 301. Origen: `/privacy`. Destino: `https://cleantechhub.net/politica-de-privacidad/`. Repita el 301 para `/privacy/`.
11. Añada el enlace en el pie. El pie es un área de widgets de Astra. Hoy solo muestra el contacto.
12. GTranslate está instalado. Si traduce todo el sitio, excluya esta página. Si no, puede volver a traducir la mitad en inglés.
13. Cuando la URL responda 200, péguela en la solicitud de LinkedIn. Hasta ese momento el campo sigue en `[GIDEON TO FILL]`.

## Qué se reutilizó de la política de 2022

La fuente es el PDF «Política y tratamiento de datos», enlazado desde `https://cleantechhub.net/governance/`. Rige desde el 1 de diciembre de 2022.

De ahí salen el responsable, el NIT, la dirección de Bogotá, los derechos de la Ley 1581 de 2012, el plazo de las consultas, la prohibición de vender los datos, y las finalidades de donantes, beneficiarios, empleados y proveedores.

Esa política es un texto interno. No está alojada en cleantechhub.net. Este borrador no la deroga. `[GIDEON TO FILL]` si esta página pública debe reemplazarla.

El PDF no trae un número del Registro Nacional de Bases de Datos. `[GIDEON TO FILL]` si ese número existe.

El correo del PDF no se lee bien. Aparece partido. El canal de reclamos del PDF es `ofcumplimiento@solucionesjv.co` y el teléfono `(+571) 313-7155965`. El sitio publica `info@cleantechhub.net` y `+57 311 4494784`. No se eligió uno. Hay que confirmar cuál recibe las solicitudes.

## Hechos del sitio que el texto sí cubre

- El pie tiene el formulario WPForms 104, título «Stay up to date». El campo visible es el correo.
- En las rutas `/diagnostico`, un script puede pedir el correo para «tips de financiamiento verde (max 1/semana)». La casilla carga marcada. Hay que dejarla sin marcar antes de publicar.
- Ese script envía el correo a `https://agents.cleantechhub.net/diagnostico/lead`.
- La portada carga Google Analytics `G-5Q0N5VB7KZ` y la etiqueta de Google Ads `AW-10974720045`.
- Polylang fija la cookie `pll_language`.
- No apareció un formulario público de empleo en el mapa del sitio ni en la búsqueda de páginas.

---

# Política de privacidad

Texto en español. La versión en inglés está al final. Si alguna frase difiere, manda el español.

Esta página explica cómo FUNDACION CLEANTECH HUB S.A.S. trata los datos personales. Cubre el sitio cleantechhub.net, el boletín, las convocatorias de empleo, y la página de LinkedIn de CleantechHUB.

Fecha de este borrador: 22 de octubre de 2026. La fecha de entrada en vigor es [GIDEON TO FILL], el día en que la página se publique.

La política interna de tratamiento de datos rige desde el 1 de diciembre de 2022. Está enlazada desde la página de gobernanza. Este texto público añade el sitio, el boletín, el empleo y LinkedIn.

## 1. Responsable del tratamiento

Responsable: FUNDACION CLEANTECH HUB S.A.S.

NIT (Número de Identificación Tributaria): 901.523.941-9.

Domicilio: Calle 90 No. 19-41 Of 801, Bogotá, D.C., Colombia.

Estos datos salen de la política interna. Hay que confirmarlos contra el RUT antes de publicar. [GIDEON TO FILL] si el RUT muestra otro nombre, otro NIT u otra dirección.

La política interna nombra a Gideon Blaauw como representante legal. [GIDEON TO FILL] el correo del representante. En el PDF ese correo no se lee con claridad.

CleantechHUB es el nombre público de esta organización.

## 2. Normas

Tratamos los datos según la Ley 1581 de 2012 y el Decreto 1377 de 2013. La política interna también cita el Decreto 886 de 2014.

Pedimos autorización previa, expresa e informada, salvo las excepciones del artículo 10 de la Ley 1581 de 2012.

La autorización puede constar por escrito, o por un acto claro de la persona. Guardamos prueba de esa autorización.

## 3. A quién aplica

Aplica a las personas que visitan el sitio, escriben al boletín, se postulan a un empleo, participan en programas, donan, proveen bienes o servicios, o aparecen en los datos de la página de LinkedIn de CleantechHUB.

También aplica a empleados, contratistas y donantes, como ya lo dice la política interna.

No está dirigida a niñas, niños ni adolescentes.

## 4. Qué datos tratamos

Tratamos solo lo que hace falta para cada fin.

**Sitio web.** Datos técnicos de la visita, como la página vista y el origen de la visita, por las etiquetas de Google descritas abajo. La cookie `pll_language` guarda el idioma.

**Boletín del pie de página.** El formulario WPForms número 104 pide el correo electrónico. El título visible es «Stay up to date».

**Tips de financiamiento verde.** En `/diagnostico`, el sitio puede pedir el correo y una casilla de autorización. El envío va a `https://agents.cleantechhub.net/diagnostico/lead`. La casilla pública carga marcada. [GIDEON TO FILL] dejarla vacía antes de publicar esta página. La autorización tiene que ser un acto de la persona.

**Empleo.** CleantechHUB puede publicar convocatorias en su sitio y en su página de LinkedIn. El 22 de octubre de 2026 no había un formulario público de postulaciones en cleantechhub.net. Si una persona envía su hoja de vida, tratamos el nombre, el contacto, la experiencia y los archivos que adjunte. El canal de recepción es [GIDEON TO FILL].

**Programas, donantes y proveedores.** La política interna ya cubre datos de contacto, datos de la relación, y la información necesaria para ejecutar convenios y contratos.

**Página de LinkedIn de CleantechHUB.** El detalle está en la sección 6. No pedimos la lista de contactos de los miembros. No armamos perfiles de miembros.

No pedimos datos sensibles en estos canales. Si una hoja de vida trae datos de salud u otros datos sensibles, [GIDEON TO FILL] la regla de borrado. La respuesta a preguntas sobre datos sensibles, o sobre datos de niñas, niños y adolescentes, es facultativa.

## 5. Para qué los usamos

Usamos los datos para estos fines.

- Publicar y administrar el sitio.
- Enviar el boletín y, si la persona lo pidió, los tips de financiamiento verde.
- Revisar una postulación y, si hay contratación, cumplir el contrato de trabajo.
- Operar los programas, informar a donantes y beneficiarios, y atender peticiones, quejas y reclamos.
- Cumplir la ley y responder a autoridades cuando la ley lo ordena.
- Medir el uso del sitio con las etiquetas de Google ya instaladas.
- Publicar contenido de CleantechHUB en su propia página de LinkedIn, y leer el resultado de esas publicaciones.

La política interna también autoriza fines administrativos, contractuales, de proveedores y de personal. Esos fines siguen vigentes para esas relaciones.

No usamos los datos de la API (interfaz de programación de aplicaciones) de LinkedIn para publicidad, ventas, reclutamiento de terceros, ni listas de audiencia.

## 6. Datos de la API de LinkedIn

CleantechHUB usa un flujo propio para su única página de LinkedIn. No gestiona páginas de otras organizaciones.

**Qué se recoge.**

- Las publicaciones que CleantechHUB crea en su página. Incluyen convocatorias, programas y boletines.
- Los comentarios que otras personas dejan en esas publicaciones, y el mínimo de datos de perfil necesario para mostrar el comentario.
- Cifras agregadas de esas publicaciones: impresiones, clics, reacciones, comentarios, compartidos y engagement.
- Cifras agregadas de la página: seguidores y vistas. Esas cifras no identifican a una persona.
- El identificador y el perfil básico de la persona administradora que autoriza la conexión.

**Para qué.**

- Publicar el contenido de CleantechHUB como la página.
- Leer las publicaciones y los comentarios de esa página.
- Ver el rendimiento agregado de ese contenido.

**Cuánto tiempo.**

- El contenido de la propia página puede guardarse hasta seis meses, porque la página se autentica en la aplicación.
- Las cifras agregadas, sin datos de una persona, pueden guardarse hasta un año.
- El nombre y el logo de la página pueden guardarse hasta ocho semanas.
- Los identificadores de la organización y de las publicaciones pueden conservarse sin un tope de LinkedIn.
- El perfil de la persona administradora que inicia sesión puede conservarse mientras la autorización siga vigente.
- El contenido de comentarios y reacciones de miembros se borra en un máximo de 48 horas.
- El nombre, la foto o el titular de un miembro que no inició sesión solo se guarda en caché hasta 24 horas. No se almacena.

**Qué no hacemos.**

- No vendemos esos datos.
- No los compartimos con anunciantes ni con otras empresas.
- No los unimos a un CRM (sistema de gestión de relaciones con clientes) ni a otra base de datos.
- No mostramos un feed de LinkedIn en cleantechhub.net ni en una intranet.
- No rastreamos miembros para armar audiencias.

Al publicar en LinkedIn, el contenido de la publicación se envía a LinkedIn. LinkedIn lo trata con sus propias reglas. El lugar donde el flujo guarda las copias es [GIDEON TO FILL].

Puede pedir el borrado por el canal de la sección 12. También borramos los datos de miembros cuando LinkedIn lo pide, y al terminar el acceso a la API.

## 7. Boletín

El pie de cleantechhub.net recoge un correo para mantener a la persona al día.

Guardamos ese correo mientras la suscripción esté activa. Lo borramos si la persona se da de baja o pide la supresión. El sistema que guarda la lista es [GIDEON TO FILL].

Los tips de financiamiento verde son un envío distinto. El máximo anunciado en el sitio es uno por semana. Hace falta una casilla que la persona marque. Hoy esa casilla carga marcada. No publique esta página hasta corregirlo.

El boletín no incluye datos de miembros recogidos por la API de LinkedIn.

## 8. Convocatorias de empleo

Las convocatorias publicadas en la página de LinkedIn, o en el sitio, son contenido de CleantechHUB.

Los datos de quien se postula se usan para ese proceso de selección. El plazo de conservación después del proceso es [GIDEON TO FILL].

Si la persona es contratada, los fines son los de la política interna: cumplir la ley laboral, administrar la relación, y dar acceso a las herramientas del trabajo.

Esas bases no se venden. No se arman con datos de miembros de LinkedIn.

## 9. Cookies y medición

La portada carga dos etiquetas de Google.

- Google Analytics: `G-5Q0N5VB7KZ`.
- Google Ads: `AW-10974720045`.

Esas etiquetas pueden guardar cookies y enviar a Google la página vista y eventos de formularios. [GIDEON TO FILL] si la etiqueta de Ads debe seguir activa.

Polylang guarda la cookie `pll_language` durante un año. Sirve para recordar el idioma. La vimos en la respuesta del sitio.

[GIDEON TO FILL] cualquier otra cookie que el administrador tenga activa y que no esté en esta lista.

## 10. Conservación

Además de los plazos de LinkedIn, estos son los plazos propios.

- Correo del boletín: mientras dure la suscripción, y se borra al pedir la baja.
- Postulaciones: [GIDEON TO FILL].
- Datos de empleados, contratistas, donantes y proveedores: el tiempo que exija la relación y la ley. [GIDEON TO FILL] el plazo contable y laboral.
- Cifras agregadas de la página de LinkedIn, sin datos de una persona: hasta un año.

Cuando un plazo de LinkedIn es más corto, manda el plazo más corto.

## 11. No vendemos ni alquilamos los datos

No vendemos, alquilamos ni cedemos las bases de datos, ni en todo ni en parte, ni gratis ni por un precio.

Así lo dice la política interna, y esta página lo mantiene.

Sí podemos entregar datos en estos casos.

- A la persona titular, cuando ejerce sus derechos.
- A una autoridad, cuando la ley colombiana lo ordena.
- A un encargado que trata datos por cuenta de CleantechHUB. La lista de encargados está en la sección 12.
- A LinkedIn, cuando publicamos en la página de CleantechHUB.
- A un aliado, solo para una actividad propia de CleantechHUB, como ya lo permite la política interna.

Los datos de miembros obtenidos por la API de LinkedIn no entran en el envío a aliados.

## 12. Encargados y transferencias

El sitio está en un servidor cuyo bloque de IP está a nombre de OVH GmbH, en Alemania. Visitar el sitio puede implicar un tratamiento fuera de Colombia.

Google recibe los datos de las etiquetas de medición. LinkedIn recibe el contenido que publicamos.

[GIDEON TO FILL] el país donde corre el flujo de n8n, y el contrato con cada encargado.

La política interna permite transferir y transmitir datos dentro y fuera de Colombia para el objeto de la organización. Esta página mantiene esa regla, con la exclusión de la sección 11 para los datos de miembros de LinkedIn.

[GIDEON TO FILL] el número de registro de bases de datos, si existe.

## 13. Derechos de las personas

La persona titular puede pedir lo siguiente.

- Conocer, actualizar y rectificar sus datos.
- Pedir prueba de la autorización, salvo cuando la ley no la exige.
- Conocer el uso que se les ha dado.
- Presentar quejas ante la Superintendencia de Industria y Comercio por un incumplimiento de la Ley 1581 de 2012.
- Revocar la autorización y pedir la supresión.
- Acceder gratis a sus datos.

Estos derechos cubren el acceso, la rectificación, la supresión y la revocatoria. Puede pedirlos la persona titular, sus causahabientes, su representante, una autoridad en ejercicio de sus funciones, o un tercero autorizado por la persona o por la ley.

La supresión no procede cuando una ley exija conservar el dato. [GIDEON TO FILL] los casos concretos, si los hay.

## 14. Cómo hacer una solicitud

Escriba a [GIDEON TO FILL].

Candidatos que ya aparecen en documentos públicos, sin elegir uno: `ofcumplimiento@solucionesjv.co`, `info@cleantechhub.net`, y el correo del representante legal.

Teléfono: [GIDEON TO FILL]. El PDF interno muestra `(+571) 313-7155965`. El sitio muestra `+57 311 4494784`.

También puede escribir a Calle 90 No. 19-41 Of 801, Bogotá, D.C.

Diga su nombre, su contacto, los datos que quiere consultar o corregir, y una descripción clara del pedido. Podemos pedir datos para confirmar que usted es el titular.

Las consultas se responden en un máximo de diez (10) días hábiles desde la recepción. Si no alcanza, se avisa el motivo y la fecha nueva. Esa prórroga no pasa de cinco (5) días hábiles.

Los reclamos se responden en un máximo de quince (15) días hábiles. Si no alcanza, se avisa el motivo y la fecha nueva. Esa prórroga no pasa de ocho (8) días hábiles. Este plazo es el de la Ley 1581 de 2012.

El trámite es gratis, salvo los casos que la ley exceptúe.

Si no está de acuerdo, puede acudir a la Superintendencia de Industria y Comercio.

El mismo canal sirve para pedir el borrado de datos de LinkedIn, del boletín o de una postulación.

## 15. Cambios

Un cambio sustancial se informa a los titulares antes de aplicarlo, de una forma que puedan conocerlo. Así lo pide la política interna, con base en el Decreto 1377 de 2013.

La fecha de la versión publicada quedará al inicio de esta página.

## 16. Contacto del responsable

FUNDACION CLEANTECH HUB S.A.S.

Calle 90 No. 19-41 Of 801, Bogotá, D.C., Colombia.

Correo: [GIDEON TO FILL].

Teléfono: [GIDEON TO FILL].

Sitio: https://cleantechhub.net

# Privacy policy

English version. Spanish controls if the two texts differ.

This page explains how FUNDACION CLEANTECH HUB S.A.S. handles personal data. It covers cleantechhub.net, the newsletter, job openings, and the CleantechHUB LinkedIn Page.

Draft date: 22 October 2026. The effective date is [GIDEON TO FILL], the day this page is published.

The internal data-processing policy has been in force since 1 December 2022. It is linked from the governance page. This public text adds the website, the newsletter, jobs, and LinkedIn.

Confirm the legal name, the tax number, and the address against the RUT (Registro Único Tributario) before publication.

## 1. Data controller

Controller: FUNDACION CLEANTECH HUB S.A.S.

NIT (Colombian tax identification number): 901.523.941-9.

Address: Calle 90 No. 19-41 Of 801, Bogotá, D.C., Colombia.

These details come from the internal policy. Confirm them against the RUT before publication. [GIDEON TO FILL] if the RUT shows another name, tax number, or address.

The internal policy names Gideon Blaauw as legal representative. [GIDEON TO FILL] the representative’s email. That line is not readable in the PDF.

CleantechHUB is the public name of this organization.

## 2. Law

We process personal data under Colombian Law 1581 of 2012 and Decree 1377 of 2013. The internal policy also cites Decree 886 of 2014.

We ask for prior, express, and informed authorization, except for the cases in article 10 of Law 1581 of 2012.

Authorization may be in writing, or by a clear act of the person. We keep proof of that authorization.

## 3. Who this covers

It covers people who visit the site, join the newsletter, apply for a job, join a program, donate, supply goods or services, or appear in data from the CleantechHUB LinkedIn Page.

It also covers employees, contractors, and donors, as the internal policy already states.

It is not directed at children.

## 4. What we process

We process only what each purpose needs.

**Website.** Technical visit data, such as the page viewed and the referrer, through the Google tags below. The `pll_language` cookie stores the language.

**Footer newsletter.** WPForms form 104 asks for an email address. The visible title is “Stay up to date.”

**Green-finance tips.** On `/diagnostico`, the site can ask for an email and a consent checkbox. The submission goes to `https://agents.cleantechhub.net/diagnostico/lead`. The public checkbox loads already checked. [GIDEON TO FILL] clear that default before this page is published. Authorization has to be the person’s own act.

**Jobs.** CleantechHUB may publish openings on its site and on its LinkedIn Page. On 22 October 2026 there was no public application form on cleantechhub.net. If a person sends a résumé, we process the name, contact details, experience, and the files they attach. The intake channel is [GIDEON TO FILL].

**Programs, donors, and suppliers.** The internal policy already covers contact details, relationship data, and the information needed to perform agreements and contracts.

**CleantechHUB LinkedIn Page.** Details are in section 6. We do not request members’ contact lists. We do not build member profiles.

We do not ask for sensitive data on these channels. If a résumé contains health data or other sensitive data, the deletion rule is [GIDEON TO FILL]. Answers about sensitive data, and about children’s data, are optional.

## 5. Why we use the data

We use the data for these purposes.

- To publish and run the website.
- To send the newsletter and, if the person asked for them, the green-finance tips.
- To review a job application and, if we hire the person, to perform the employment contract.
- To run programs, inform donors and beneficiaries, and handle requests and complaints.
- To comply with the law, and to answer authorities when the law requires it.
- To measure site use with the Google tags already installed.
- To publish CleantechHUB content on its own LinkedIn Page, and to read the results of those posts.

The internal policy also allows administrative, contractual, supplier, and staff purposes. Those purposes remain in force for those relationships.

We do not use LinkedIn application programming interface (API) data for advertising, sales, third-party recruiting, or audience lists.

## 6. LinkedIn API data

CleantechHUB uses its own workflow for its single LinkedIn Page. It does not manage any other organization’s Page.

**What is collected.**

- Posts CleantechHUB creates on its Page. They include job openings, programs, and newsletters.
- Comments other people leave on those posts, and the minimum profile data needed to display the comment.
- Aggregate figures for those posts: impressions, clicks, reactions, comments, shares, and engagement.
- Aggregate Page figures: followers and views. Those figures do not identify a person.
- The identifier and basic profile of the admin who authorizes the connection.

**Purpose.**

- To publish CleantechHUB content as the Page.
- To read that Page’s posts and comments.
- To see the aggregate performance of that content.

**Retention.**

- The Page’s own content may be stored for up to six months, because the Page signs in to the application.
- Aggregate figures, with no data about a person, may be stored for up to one year.
- The Page name and logo may be stored for up to eight weeks.
- Identifiers for the organization and the posts may be kept with no LinkedIn time cap.
- The signed-in admin’s profile may be kept while the authorization remains in force.
- The content of member comments and reactions is deleted within 48 hours.
- A non-signed-in member’s name, photo, or headline is cached for at most 24 hours. It is not stored.

**What we do not do.**

- We do not sell this data.
- We do not share it with advertisers or with other companies.
- We do not combine it with a customer relationship management (CRM) system or with any other database.
- We do not show a LinkedIn feed on cleantechhub.net or on an intranet.
- We do not track members to build audiences.

When we publish to LinkedIn, the post content is sent to LinkedIn. LinkedIn processes it under LinkedIn’s own rules. The place where the workflow stores copies is [GIDEON TO FILL].

You can ask for deletion through the channel in section 12. We also delete member data when LinkedIn asks, and when API access ends.

## 7. Newsletter

The cleantechhub.net footer collects an email address so we can keep the person up to date.

We keep that email while the subscription is active. We delete it if the person unsubscribes or asks for erasure. The system that stores the list is [GIDEON TO FILL].

The green-finance tips are a separate send. The site states a maximum of one a week. The person must check a box. That box currently loads already checked. Do not publish this page until that is fixed.

The newsletter does not include member data collected through the LinkedIn API.

## 8. Job openings

Openings published on the LinkedIn Page, or on the site, are CleantechHUB content.

Applicant data is used for that selection process. The retention period after the process is [GIDEON TO FILL].

If the person is hired, the purposes are those in the internal policy. They are to comply with employment law, to administer the relationship, and to give access to work tools.

Those databases are not sold. They are not built from LinkedIn member data.

## 9. Cookies and measurement

The homepage loads two Google tags.

- Google Analytics: `G-5Q0N5VB7KZ`.
- Google Ads: `AW-10974720045`.

Those tags can store cookies and send Google the page viewed and form events. [GIDEON TO FILL] whether the Ads tag should stay on.

Polylang stores the `pll_language` cookie for one year. It remembers the language. We saw it on the site response.

[GIDEON TO FILL] any other cookie the administrator has enabled that is not on this list.

## 10. Retention

Besides the LinkedIn periods, these are our own periods.

- Newsletter email: for as long as the subscription lasts, then deleted on unsubscribe.
- Applications: [GIDEON TO FILL].
- Employee, contractor, donor, and supplier data: for as long as the relationship and the law require. [GIDEON TO FILL] the accounting and employment periods.
- Aggregate LinkedIn Page figures, with no data about a person: up to one year.

When a LinkedIn period is shorter, the shorter period applies.

## 11. We do not sell or rent the data

We do not sell, rent, or assign the databases, in whole or in part, for free or for a price.

The internal policy says this, and this page keeps it.

We may disclose data in these cases.

- To the person, when they use their rights.
- To an authority, when Colombian law requires it.
- To a processor that handles data for CleantechHUB. The processor list is in section 12.
- To LinkedIn, when we publish on the CleantechHUB Page.
- To a partner, only for an activity of CleantechHUB, as the internal policy already allows.

Member data obtained through the LinkedIn API is excluded from disclosure to partners.

## 12. Processors and transfers

The site runs on a server whose IP block is registered to OVH GmbH, in Germany. Visiting the site can mean processing outside Colombia.

Google receives the measurement-tag data. LinkedIn receives the content we publish.

[GIDEON TO FILL] the country where the n8n workflow runs, and the contract with each processor.

The internal policy allows transfers inside and outside Colombia for the organization’s purpose. This page keeps that rule, with the section 11 exclusion for LinkedIn member data.

[GIDEON TO FILL] the database-registry number, if one exists.

## 13. People’s rights

The person can ask for the following.

- To know, update, and rectify their data.
- Proof of authorization, except where the law does not require it.
- To know the use given to their data.
- To complain to the Superintendence of Industry and Commerce about a breach of Law 1581 of 2012.
- To revoke authorization and ask for deletion.
- Free access to their data.

These rights cover access, rectification, deletion, and revocation. They can be used by the person, their heirs, their representative, an authority acting in its functions, or a third party authorized by the person or by the law.

Deletion does not apply when a law requires the data to be kept. [GIDEON TO FILL] the concrete cases, if any.

## 14. How to make a request

Write to [GIDEON TO FILL].

Candidates that already appear in public documents, with none selected: `ofcumplimiento@solucionesjv.co`, `info@cleantechhub.net`, and the legal representative’s email.

Phone: [GIDEON TO FILL]. The internal PDF shows `(+571) 313-7155965`. The website shows `+57 311 4494784`.

You can also write to Calle 90 No. 19-41 Of 801, Bogotá, D.C.

State your name, your contact details, the data you want to see or correct, and a clear description of the request. We may ask for information to confirm that you are the holder.

Consultations are answered within ten (10) business days of receipt. If that is not possible, we explain why and give a new date. The extension is no more than five (5) business days.

Complaints are answered within fifteen (15) business days. If that is not possible, we explain why and give a new date. The extension is no more than eight (8) business days. This period is the one in Law 1581 of 2012.

The process is free, except where the law says otherwise.

If you disagree, you can go to the Superintendence of Industry and Commerce.

The same channel is how you ask us to delete LinkedIn data, newsletter data, or an application.

## 15. Changes

A material change is communicated to the holders before it applies, in a way they can actually learn about it. The internal policy requires this, based on Decree 1377 of 2013.

The date of the published version will appear at the top of this page.

## 16. Controller contact

FUNDACION CLEANTECH HUB S.A.S.

Calle 90 No. 19-41 Of 801, Bogotá, D.C., Colombia.

Email: [GIDEON TO FILL].

Phone: [GIDEON TO FILL].

Website: https://cleantechhub.net
