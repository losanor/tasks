async def relatorio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tarefas = supabase.table("tarefas").select("*").execute().data
    total = len(tarefas)
    status_map = {}
    class_map = {}
    aging_map = {}
    hoje = datetime.now()
    for t in tarefas:
        s = t["status"]
        c = t["classificacao"]
        status_map[s] = status_map.get(s, 0) + 1
        class_map[c] = class_map.get(c, 0) + 1
        if t["status"] == "Finalizada" and t.get("data_finalizacao"):
            dt_ini = datetime.fromisoformat(t["data_criacao"])
            dt_fim = datetime.fromisoformat(t["data_finalizacao"])
            dias = (dt_fim - dt_ini).days
            aging_map[c] = aging_map.get(c, []) + [dias]
    msg = f"📊 Relatório ({total} tarefas):\n\n"
    msg += "Por status:\n" + "\n".join([f"{k}: {v}" for k, v in status_map.items()]) + "\n\n"
    msg += "Por classificação:\n" + "\n".join([f"{k}: {v}" for k, v in class_map.items()]) + "\n\n"
    msg += "Aging médio (dias):\n"
    for k, v in aging_map.items():
        media = round(sum(v)/len(v), 2)
        msg += f"{k}: {media} dias\n"
    await update.message.reply_text(msg)
