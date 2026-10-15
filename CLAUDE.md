# AI Engineer — sistema de estudo

Este projeto é o ambiente de estudo de AI engineering do usuário. Adaptado do sistema
[amosblomqvist/learn](https://github.com/amosblomqvist/learn) (feito para o pi) para o Claude Code.

## O aprendiz
- Estudando para atuar como AI engineer; faz uma mentoria de AI engineering com aulas curtas e longas, muito densas.
- Lê e estuda no Obsidian; consolida conhecimento desenhando à mão (Excalidraw + mesa digitalizadora).

## Idioma
Aulas, notas e quizzes em **português do Brasil**. Termos técnicos consagrados ficam em inglês
(attention, embedding, retrieval, fine-tuning…), com tradução na primeira menção se ajudar.

## Onde as coisas vivem
- **Vault (conteúdo):** `~/Documents/AI Engineering/` — estrutura descrita em `00 Mapa.md`; modelos em `Templates/`.
- **Currículo (fonte, fora do vault):** `curriculum/` — clone do [ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch). Aula = `phases/<fase>/<aula>/docs/en.md` + `code/` + `quiz.json`. Atualizar com `git -C curriculum pull`.
- **Prática do currículo:** `pratica/<fase>/<aula>/` — o código que o aprendiz digita (nunca dentro de `curriculum/`).
- **Progresso do currículo:** `LEARNING.md` (raiz do projeto), criado por `/nivelamento` — a *Study queue* é a ordem de estudo, aula a aula: um **roteiro integrado** em etapas que mistura itens `mentoria:` (semanas da mentoria) com aulas do currículo, mais 1–2 aulas de base por etapa (ritmo 2:1).
- **Ferramentas:** `.claude/tools/` — `quiz.py`, `md_log.py`, `import_transcript.py`, `drawing.py`, `render.sh`, `placement.py` + `strands.json` (vertentes do nivelamento), `status.py` (estado do sistema), `open_note.py` (abre uma nota no Obsidian — a "lousa" das aulas); `.claude/state/` guarda arquivos de execução (log de quizzes, vínculos do md-log).

## Skills e agentes
| Skill | Para quê |
|---|---|
| `/manual` | Explica o sistema, mostra o estado atual e sugere o próximo passo |
| `teach` | O método — toda explicação e toda sessão de estudo |
| `/mentoria` | Importar transcript da mentoria e estudar a aula bloco a bloco (`/mentoria continuar`) |
| `/curriculo` | Próxima aula (ou uma aula específica) do currículo |
| `/nivelamento` | Nivelamento adaptativo por vertente → `LEARNING.md` + nota no vault (`continuar`, `refazer`) |
| `/guia-curso` · `/prova-fase` | Achar a aula de um tema · prova de uma fase |
| `/desenho` · `/revisar-desenho` | Consolidação desenhando de memória no Excalidraw |
| `/md-log` | Espelhar a sessão numa nota do vault |
| `visualize` | Diagramas (Mermaid inline ou via `mermaid-maker` / `svg-maker`) |

Agentes: `researcher` (verificação de fatos), `mermaid-maker`, `svg-maker`.

Os skills que vêm dentro de `curriculum/.claude/skills/` **não** são usados diretamente — em especial o `learn` do repo (o `/curriculo` substitui). `/guia-curso` e `/prova-fase` leem os originais e aplicam ajustes; o `/nivelamento` é próprio (o `find-your-level` do repo é raso demais).

## Regras
- Qualquer explicação ou aula segue o skill `teach`.
- Perguntas com resposta certa vão por `quiz.py`; perguntas sem resposta certa (preferência, direção) vão por AskUserQuestion.
- Fatos de que não tiver certeza: confirme com o subagente `researcher` antes de afirmar.
- Matemática sempre em LaTeX (`$...$`, `$$...$$`) — o Obsidian renderiza.
- Conteúdo do vault é do usuário: atualize notas existentes acrescentando, sem apagar o que ele escreveu. Transcripts em `Fontes/` nunca são editados.
