import { useEffect, useState } from "react";
import Nav from "../components/Nav";
import { apiGet, apiPatch } from "../utils/api";
import { DndContext, closestCenter } from "@dnd-kit/core";
import { arrayMove, SortableContext, verticalListSortingStrategy, useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

const STAGES = ["new","qualified","won","lost"];

function Card({ id, title, amount }) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id });
  const style = { transform: CSS.Transform.toString(transform), transition };
  return <div ref={setNodeRef} style={style} {...attributes} {...listeners} className="p-2 mb-2 bg-white rounded shadow">{title} — ₹{amount}</div>;
}

export default function Kanban() {
  const [cols, setCols] = useState({ new: [], qualified: [], won: [], lost: [] });

  async function load() {
    const data = await apiGet("/api/deals/");
    const items = (data.results || []).map(d => ({ id: d.id.toString(), title: d.title, amount: d.amount, stage: d.stage }));
    const grouped = { new: [], qualified: [], won: [], lost: [] };
    items.forEach(i => grouped[i.stage].push(i));
    setCols(grouped);
  }
  useEffect(() => { load(); }, []);

  async function onDragEnd(event) {
    const { active, over } = event;
    if (!over) return;
    const [fromStage, toStage] = active.data.current?.stage && over.id ? [active.data.current.stage, over.id] : [null, null];
    if (!fromStage || !toStage) return;
    if (fromStage === toStage) return;
    const card = cols[fromStage].find(c => c.id === active.id);
    // optimistic UI
    setCols(prev => {
      const from = prev[fromStage].filter(c => c.id !== active.id);
      const to = [{ ...card, stage: toStage }, ...prev[toStage]];
      return { ...prev, [fromStage]: from, [toStage]: to };
    });
    try { await apiPatch(`/api/deals/${card.id}/`, { stage: toStage }); }
    catch { load(); }
  }

  return (
    <main className="max-w-6xl mx-auto p-4 font-sans">
      <Nav />
      <h2 className="text-2xl font-semibold mb-4">Deals Kanban</h2>
      <DndContext collisionDetection={closestCenter} onDragEnd={onDragEnd}>
        <div className="grid grid-cols-4 gap-4">
          {STAGES.map(stage => (
            <Column key={stage} id={stage} title={stage} items={cols[stage]} />
          ))}
        </div>
      </DndContext>
    </main>
  );
}

function Column({ id, title, items }) {
  return (
    <div id={id} className="bg-gray-50 rounded p-3 min-h-[300px]">
      <h3 className="capitalize font-medium mb-2">{title}</h3>
      <SortableContext items={items.map(i => i.id)} strategy={verticalListSortingStrategy}>
        {items.map(i => <DraggableCard key={i.id} stage={id} {...i} />)}
      </SortableContext>
    </div>
  );
}

function DraggableCard(props) {
  const { id, title, amount, stage } = props;
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id, data: { stage } });
  const style = { transform: CSS.Transform.toString(transform), transition };
  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners} className="p-2 mb-2 bg-white rounded shadow cursor-move">
      {title} — ₹{amount}
    </div>
  );
}
