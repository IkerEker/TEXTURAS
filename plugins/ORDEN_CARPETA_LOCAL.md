# ORDEN 2 · Dejar GitHub y trabajar solo desde la carpeta Biblioteca del ordenador de Iker

*(Iker: pega este texto entero en la conversación de cada plugin, después de la ORDEN 1 (`ORDEN_PLUGINS.md`).
Antes, en esa conversación, conecta la carpeta: ábrela en la app de escritorio de Claude en tu PC → botón **+** →
**Añadir carpeta** → `C:\Users\ikerg\Biblioteca`. Es la única carpeta que hace falta. Si la conversación te pide permiso
para esa carpeta, acéptalo.)*

---

**Esta orden es de Iker y es permanente.** A partir de ahora tu plugin vive en el ordenador de Iker, dentro de
`C:\Users\ikerg\Biblioteca`, y no en GitHub.

Objetivos:
1. Que no se pierda nada: código, historial, ramas, pruebas ni herramientas.
2. Que no haya archivos repetidos: el material está una sola vez, en la biblioteca.
3. Que siempre encuentres todo con el buscador de la biblioteca.

Copia el apartado «REGLAS PERMANENTES» del final a tu `CLAUDE.md`. Después haz los pasos en orden y dame el informe.

## 0. Acceso

- Necesitas la carpeta `C:\Users\ikerg\Biblioteca` conectada a esta conversación. Comprueba que la ves, por ejemplo
  listándola.
- Si no la ves, pídela con la herramienta de acceso a carpetas, solo esa ruta, o dime que la conecte con
  **+ → Añadir carpeta**.
- No pidas ninguna otra carpeta del ordenador.
- Si tienes terminal en el ordenador de Iker, trabaja con ella dentro de la Biblioteca.
- Si no la tienes, prepara los comandos exactos en un `.bat` dentro de tu carpeta y dime que lo ejecute. No inventes
  rutas.

## 1. Dónde va cada cosa

```
C:\Users\ikerg\Biblioteca\
├── TEXTURAS\            la biblioteca (índice, buscador, fichas). Antes de nada: git pull (rama atlas)
├── ACIDBITE\  originales\  generadas\     material (no se toca)
├── _fuentes\<repo>\     copias que se hicieron para montar la biblioteca (no las borres tú)
└── plugins\
    ├── <tu-plugin>\     ← TU CASA: el repo completo, con su .git, todas las ramas y etiquetas
    └── _respaldos\      ← <tu-plugin>_AAAA-MM-DD.bundle (copia de seguridad de todo el historial)
```

## 2. Copia completa y comprobada (antes de dejar GitHub)

1. **Actualiza la biblioteca:** `git -C Biblioteca\TEXTURAS pull origin atlas`.
2. **Sube lo que tengas sin subir.** Si tu sesión tiene cambios o ramas que no están en GitHub, haz commit y push
   primero. Nada puede quedarse solo en tu sesión en la nube.
3. **Clona todo en la casa nueva:**
   `git clone --no-single-branch <url de tu repo> Biblioteca\plugins\<tu-plugin>`
   y después `git fetch --all --tags`. Crea en local una rama por cada rama remota.
4. **Haz la copia de seguridad del historial:**
   `git bundle create Biblioteca\plugins\_respaldos\<tu-plugin>_<fecha>.bundle --all`
   y compruébala con `git bundle verify`.
5. **Comprueba que no falta nada:**
   - lista ramas, etiquetas y último commit de cada rama en GitHub y en local: tienen que coincidir uno a uno;
   - lista los archivos de GitHub (`git ls-tree -r` de cada rama) y compáralos con los locales;
   - si hay Git LFS, descarga los objetos (`git lfs fetch --all`) y compruébalos.
6. **Mira lo que no está en git pero lo necesitas**, por ejemplo `dist/`, `.ccx` construidos o anexos de tu ficha.
   Cópialo a tu casa nueva y anótalo.

## 3. Sin repetidos: el material sale de la biblioteca

1. Si aún no lo hiciste (ORDEN 1, parte A), haz que tu construcción lea el material **por id** desde
   `Biblioteca\TEXTURAS\indice\indice.json`. Pasa tu **prueba exacta** antes y después: tiene que dar idéntico.
2. Calcula el md5 de cada archivo de material de tu casa nueva (imágenes, vídeos, sonidos, `.bin` de origen) y busca
   ese md5 en el índice.
   - Si ya está en la biblioteca y tu construcción lo lee por id, el de tu carpeta es un **repetido**: apúntalo en
     `plugins\<tu-plugin>\REPETIDOS.md` (ruta, md5, id de la biblioteca).
   - Si NO está en la biblioteca, es material nuevo: termina tu respuesta con un **PEDIDO PARA LA BIBLIOTECA** para que
     se añada y revise. No lo borres.
3. Quita los repetidos de tu carpeta, en una rama `sin-repetidos`, y solo cuando:
   - la prueba exacta pase leyendo de la biblioteca;
   - Iker apruebe borrar (te saldrá un permiso de borrado; si no lo hay, muévelos a `_para_borrar\` dentro de tu casa
     y dile a Iker cuáles son).
   El historial de git conserva todo igualmente.
4. Nunca toques nada fuera de `plugins\<tu-plugin>\`, salvo lo que añadas en `generadas\`. En concreto, no toques:
   - los demás plugins;
   - `TEXTURAS`, `ACIDBITE` y `originales`;
   - `_fuentes`.

## 4. Trabajar desde ahora

- Tu código está en `Biblioteca\plugins\<tu-plugin>\`. Usa **git en local**: un commit por cambio, ramas para lo que
  sea grande, y nunca reescribas el historial.
- Ya no hay `push` a GitHub.
- Después de cada sesión de trabajo, renueva el bundle en `_respaldos\` (guarda los 3 últimos).
- Construye y prueba en el ordenador de Iker. El plugin construido sigue funcionando solo, sin Claude ni internet.
- Para material, usa siempre el método de búsqueda de la ORDEN 1 (`buscar.py`): varias palabras, `--resumen`,
  familias, `--parecidos` y mirar la hoja. Así encuentras todo lo útil, también lo que antes se te escapaba.

## 5. Informe y permiso para borrar GitHub

Termina con este informe. Iker borra el repo de GitHub solo si dice «VERIFICADO» en todo:

```
PLUGIN: <nombre>     CASA: C:\Users\ikerg\Biblioteca\plugins\<tu-plugin>
- Ramas/etiquetas GitHub = local: <n>/<n>  VERIFICADO / FALTA …
- Último commit de cada rama coincide: VERIFICADO / …
- Archivos de cada rama coinciden: VERIFICADO / …
- Bundle creado y verificado: <ruta>  VERIFICADO / …
- Fuera de git copiado (dist, .ccx…): <lista>  VERIFICADO / …
- Construcción desde la casa nueva + prueba exacta: idéntico  VERIFICADO / …
- Material leído por id de la biblioteca: <n> ids  VERIFICADO / …
- Repetidos encontrados: <n> (<MB>); quitados: <n>; pendientes de permiso: <n>
- Pedidos para la biblioteca: <n>
→ LISTO PARA BORRAR EL REPO DE GITHUB: SÍ / NO (motivo)
```

**Tú no borras el repo de GitHub**: lo hace Iker, a mano, cuando todo esté verificado.

## REGLAS PERMANENTES (copiar al `CLAUDE.md` del plugin)

```
## Casa local (orden de Iker, 20-11-2026; texto: TEXTURAS/plugins/ORDEN_CARPETA_LOCAL.md)
- El plugin vive en C:\Users\ikerg\Biblioteca\plugins\<plugin>\ (git local, sin GitHub). Única carpeta conectada: Biblioteca.
- Copia de seguridad: git bundle --all en Biblioteca\plugins\_respaldos\ tras cada sesión (guardar 3).
- Material SOLO por id desde Biblioteca\TEXTURAS (buscar.py, método de la ORDEN 1); nada repetido dentro del plugin.
  Lo nuevo → «PEDIDO PARA LA BIBLIOTECA».
- No tocar otros plugins, TEXTURAS, ACIDBITE, originales ni _fuentes. Borrar solo con permiso de Iker.
- Prueba exacta antes y después de cada cambio. El plugin construido funciona solo, sin Claude ni internet.
```
