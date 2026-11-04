<script setup>

const props = defineProps({
    modelValue: {
        type: Number,
        default: 1
    },
    min: {
        type: Number,
        default: 1
    },
    max: {
        type: Number,
        default: 99
    }
})

const emit = defineEmits(['update:modelValue'])

function increment(){
    if(props.modelValue < props.max){
        emit('update:modelValue', props.modelValue + 1)
    }
}

function decrement(){
    if(props.modelValue > props.min){
        emit('update:modelValue', props.modelValue - 1)
    }
}

</script>

<template>
    <div class="quantity-selector">
        <button type="button" @click="decrement" :disabled="modelValue <= min" class="qty-btn" aria-label="Decrease Quantity">-</button>
        <span class="qty-display">{{ modelValue }}</span>
        <button type="button" @click="increment" :disabled="modelValue >= max" class="qty-btn" aria-label="Increase Quantity">+</button>
        
    </div>
</template>

<style scoped>

.quantity-selector{
    display: inline-flex;
    align-items: center;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    background: var(--bg-surface);
    overflow: hidden;    
}

.qty-btn{
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-main);
    background: var(--bg-page);
    transition: background 0.15s;
}

.qty-btn:hover:not(:disabled){
    background: var(--border-color);
}

.qty-btn:disabled{
    opacity: 0.4;
    cursor: not-allowed;
}

.qty-display{
    min-width: 40px;
    text-align: center;
    font-weight: 700;
    font-size: 0.95rem;
}

</style>