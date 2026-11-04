<!-- frontend/app/components/AddressFormModal.vue -->
<template>
    <div v-if="isOpen" class="modal-backdrop" @click.self="close">
        <div class="modal-card">
            <div class="modal-header">
                <h3>{{ isEditing ? 'Edit Delivery Address' : 'Add New Delivery Address' }}</h3>
                <button type="button" @click="close" class="btn-close">&times;</button>
            </div>

            <div v-if="error" class="modal-error">{{ error }}</div>

            <form @submit.prevent="handleSubmit" class="address-form">
                <div class="form-row">
                    <div class="form-group">
                        <label for="recipient">Full Name *</label>
                        <input id="recipient" v-model="form.recipient_name" type="text" required
                            placeholder="e.g. John Doe" />
                    </div>

                    <div class="form-group">
                        <label for="phone">Phone Number *</label>
                        <input id="phone" v-model="form.phone" type="tel" required placeholder="+1 (555) 000-0000" />
                    </div>
                </div>

                <div class="form-group">
                    <label for="addr1">Address Line 1 *</label>
                    <input id="addr1" v-model="form.address_line_1" type="text" required
                        placeholder="Street address, P.O. box, company name" />
                </div>

                <div class="form-group">
                    <label for="addr2">Address Line 2 (Optional)</label>
                    <input id="addr2" v-model="form.address_line_2" type="text"
                        placeholder="Apartment, suite, unit, building, floor" />
                </div>

                <div class="form-row three-col">
                    <div class="form-group">
                        <label for="city">City *</label>
                        <input id="city" v-model="form.city" type="text" required placeholder="City" />
                    </div>

                    <div class="form-group">
                        <label for="state">State / Province *</label>
                        <input id="state" v-model="form.state" type="text" required placeholder="State" />
                    </div>

                    <div class="form-group">
                        <label for="zip">Postal Code *</label>
                        <input id="zip" v-model="form.postal_code" type="text" required
                            placeholder="ZIP / Postal code" />
                    </div>
                </div>

                <div class="form-group">
                    <label for="country">Country *</label>
                    <input id="country" v-model="form.country" type="text" required placeholder="Country" />
                </div>

                <div class="checkbox-group">
                    <label class="checkbox-label">
                        <input type="checkbox" v-model="form.is_default" />
                        <span>Set as default shipping address</span>
                    </label>
                </div>

                <div class="modal-footer">
                    <button type="button" @click="close" class="btn-cancel">Cancel</button>
                    <button type="submit" class="btn-save" :disabled="submitting">
                        {{ submitting ? 'Saving...' : 'Save Address' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false
    },
    initialData: {
        type: Object,
        default: null
    }
})

const emit = defineEmits(['close', 'saved'])

const isEditing = computed(() => !!props.initialData?.id)
const submitting = ref(false)
const error = ref('')

const form = reactive({
    recipient_name: '',
    phone: '',
    address_line_1: '',
    address_line_2: '',
    city: '',
    state: '',
    postal_code: '',
    country: 'United States',
    is_default: false
})

watch(() => props.initialData, (newVal) => {
    if (newVal) {
        Object.assign(form, {
            recipient_name: newVal.recipient_name || '',
            phone: newVal.phone || '',
            address_line_1: newVal.address_line_1 || '',
            address_line_2: newVal.address_line_2 || '',
            city: newVal.city || '',
            state: newVal.state || '',
            postal_code: newVal.postal_code || '',
            country: newVal.country || 'United States',
            is_default: !!newVal.is_default
        })
    } else {
        resetForm()
    }
}, { immediate: true })

function resetForm() {
    Object.assign(form, {
        recipient_name: '',
        phone: '',
        address_line_1: '',
        address_line_2: '',
        city: '',
        state: '',
        postal_code: '',
        country: 'United States',
        is_default: false
    })
    error.value = ''
}

function close() {
    resetForm()
    emit('close')
}

const { addAddress, updateAddress } = useAccountApi()

async function handleSubmit() {
    submitting.value = true
    error.value = ''

    try {
        if (isEditing.value) {
            await updateAddress(props.initialData.id, form)
        } else {
            await addAddress(form)
        }
        emit('saved')
        close()
    } catch (err) {
        error.value = err.message || 'Failed to save address.'
    } finally {
        submitting.value = false
    }
}
</script>

<style scoped>
.modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 200;
    padding: 1.5rem;
}

.modal-card {
    background: var(--bg-surface);
    border-radius: var(--radius-lg);
    width: 100%;
    max-width: 580px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: var(--shadow-lg);
    padding: 2rem;
}

.modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}

.modal-header h3 {
    font-size: 1.25rem;
    font-weight: 800;
}

.btn-close {
    font-size: 1.5rem;
    color: var(--text-muted);
    line-height: 1;
}

.modal-error {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #b91c1c;
    padding: 0.75rem;
    border-radius: var(--radius-sm);
    font-size: 0.85rem;
    margin-bottom: 1.25rem;
}

.address-form {
    display: flex;
    flex-direction: column;
    gap: 1.15rem;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.form-row.three-col {
    grid-template-columns: 1fr 1fr 1fr;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
}

label {
    font-size: 0.85rem;
    font-weight: 600;
}

input {
    border: 1px solid var(--border-color);
    padding: 0.65rem 0.8rem;
    border-radius: var(--radius-sm);
    font-size: 0.9rem;
    outline: none;
}

input:focus {
    border-color: var(--primary);
}

.checkbox-group {
    margin-top: 0.25rem;
}

.checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
}

.modal-footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.75rem;
    margin-top: 1.5rem;
    border-top: 1px solid var(--border-color);
    padding-top: 1.25rem;
}

.btn-cancel {
    padding: 0.65rem 1.25rem;
    font-size: 0.9rem;
    font-weight: 600;
    border-radius: var(--radius-sm);
    background: var(--bg-page);
    border: 1px solid var(--border-color);
}

.btn-save {
    padding: 0.65rem 1.5rem;
    font-size: 0.9rem;
    font-weight: 600;
    border-radius: var(--radius-sm);
    background: var(--primary);
    color: #fff;
}

.btn-save:hover:not(:disabled) {
    background: var(--primary-hover);
}

@media (max-width: 600px) {

    .form-row,
    .form-row.three-col {
        grid-template-columns: 1fr;
    }
}
</style>
